import logging

from rest_framework.exceptions import APIException, ValidationError, ParseError, AuthenticationFailed, NotAuthenticated, PermissionDenied, NotFound, MethodNotAllowed, NotAcceptable, UnsupportedMediaType, Throttled
from rest_framework.views import exception_handler as base_exception_handler
from rest_framework import status

logger = logging.getLogger('logger')


class ErrorCode:
    """
    [0-2]: HTTP status code
    [3-5]: Random number
    """
    VALIDATION_ERROR         = -400001       # 유효성 검사 실패
    PARSE_ERROR              = -400002       # Malformed request
    UNHANDLED_EXCEPTION      = -400003       # Unhandled exception
    CUSTOM_EXCEPTION         = -400004       # Custom exception
    AUTHENTICATION_FAILED    = -401001       # Incorrect authentication credentials
    NOT_AUTHENTICATED        = -401002       # Authentication credentials were not provieded
    PERMISSION_DENIED        = -403005       # Do not have permission to perform the action
    NOT_FOUND                = -404006       # Not Found
    METHOD_NOT_ALLOWED       = -405007       # Method not allowed
    NOT_ACCEPTABLE           = -406008       # Could not satisfy the request Accept header
    UNSUPPORTED_MEDIA_TYPE   = -415009       # Unsupported media type in request
    TOO_MANY_REQUESTS        = -429010       # Request was throttled


def exception_handler(exc, context):
    response = base_exception_handler(exc, context)

    if isinstance(exc, ValidationError):
        invalid_fields = []
        error_message = None

        if isinstance(response.data, list):
            for index, error_data in enumerate(response.data):
                for key, value in error_data.items():
                    logger.info('name: [{}, {}], message: {}'.format(index, key, value))
                    # field
                    if key == 'non_field_errors':
                        error_message = value
                        break

                    invalid_fields.append({'name': [index, key], 'message': value[0]})
        else:
            error_data = response.data
            for key, value in error_data.items():
                logger.info('name: {}, message: {}'.format(key, value))
                # field
                if key == 'non_field_errors':
                    error_message = value
                    break

                invalid_fields.append({'name': key, 'message': value[0]})

        if error_message:
            response.data = {'error_code': ErrorCode.VALIDATION_ERROR, 'error_message': error_message}
        else:
            response.data = {'error_code': ErrorCode.VALIDATION_ERROR, 'invalid_fields': invalid_fields}

    if isinstance(exc, ParseError):  # status_code: 400
        response.data = {'error_code': ErrorCode.PARSE_ERROR, 'error_message': exc.detail}

    if isinstance(exc, AuthenticationFailed):  # status_code: 401
        response.data = {'error_code': ErrorCode.AUTHENTICATION_FAILED, 'error_message': exc.detail}

    if isinstance(exc, NotAuthenticated):  # status_code: 401
        response.data = {'error_code': ErrorCode.NOT_AUTHENTICATED, 'error_message': exc.detail}

    if isinstance(exc, PermissionDenied):  # status_code: 403
        response.data = {'error_code': ErrorCode.PERMISSION_DENIED, 'error_message': exc.detail}

    if isinstance(exc, NotFound):  # status_code: 404
        response.data = {'error_code': ErrorCode.NOT_FOUND, 'error_message': exc.detail}

    if isinstance(exc, MethodNotAllowed):  # status_code: 405
        response.data = {'error_code': ErrorCode.METHOD_NOT_ALLOWED, 'error_message': exc.detail}

    if isinstance(exc, NotAcceptable):  # status_code: 406
        response.data = {'error_code': ErrorCode.NOT_ACCEPTABLE, 'error_message': exc.detail}

    if isinstance(exc, UnsupportedMediaType):  # status_code: 415
        response.data = {'error_code': ErrorCode.UNSUPPORTED_MEDIA_TYPE, 'error_message': exc.detail}

    if isinstance(exc, Throttled):  # status_code: 429
        response.data = {'error_code': ErrorCode.TOO_MANY_REQUESTS, 'error_message': exc.detail}

    # TODO: ValueError (from codes within Models)

    if response is not None and 'error_code' not in response.data:
        if isinstance(exc, APIException): #Custom Exception
            response.data = {'error_code': ErrorCode.CUSTOM_EXCEPTION, 'error_message': exc.detail}
            response.status_code = status.HTTP_400_BAD_REQUEST
        else:
            response.data = {'error_code': ErrorCode.UNHANDLED_EXCEPTION, 'error_message': '{}'.format(exc)}

    return response

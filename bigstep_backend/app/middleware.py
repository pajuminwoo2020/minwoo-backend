import pytz
import time
import logging
from django.conf import settings
from django.utils import timezone
from app.common.logger import Logger


class TimeZoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # set timezone before creating response (so that user's timezone is used in templates)
        if request.user.is_authenticated:
            timezone.activate(pytz.timezone(request.user.timezone))
        else:
            timezone.activate(pytz.timezone(settings.TIME_ZONE))
        ### Processes request
        response = self.get_response(request)

        return response


class LoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger = logging.getLogger('logger_simple')
        request_log, user_id = Logger.make_log_str_with_request(request)
        logger.debug(f'[REQUEST] - {request_log}')
        start = time.time()

        ### Processes request
        response = self.get_response(request)

        response_log = Logger.make_log_str_with_response(response, request.path, user_id)
        end = time.time()
        logger.debug(f'[RESPONSE] - {response_log}', extra={'duration': end - start})

        return response

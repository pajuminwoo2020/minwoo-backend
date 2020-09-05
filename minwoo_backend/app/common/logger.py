import json
import logging
import chardet


class Logger:
    @staticmethod
    def get_logger():
        return logging.getLogger('logger')

    @staticmethod
    def make_log_str_with_request(request):
        user_id = 'anonymous'
        if not request.user.is_anonymous:
            user_id = request.user.id
        request_log_params = {
            'method': request.method,
            'user_id': user_id,
            'request_url': request.META.get("HTTP_HOST", "NOHOST") + request.path,
        }

        return json.dumps(request_log_params, ensure_ascii=False).replace('\\"', '"'), user_id

    @staticmethod
    def make_log_str_with_response(response, request_url, user_id):
        response_log_params = {
            'user_id': user_id,
            'status_code': response.status_code,
            'request_url': request_url
        }
        try:
            if response.has_header('Content-Type') and 'application/json' == response.__getitem__('Content-Type'):
                encoding = chardet.detect(response.content).get('encoding', 'utf-8')
                if encoding is None or encoding == 'ascii':
                    encoding = 'unicode_escape'
                body = response.content.decode(encoding)
                if len(body) > 0 and 'swagger' not in body:
                    response_log_params['response'] = body
        except Exception as e:
            response_log_params['response'] = str(e)

        return json.dumps(response_log_params, ensure_ascii=False).replace('\\"', '"')

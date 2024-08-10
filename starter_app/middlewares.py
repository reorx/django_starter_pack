import pydantic
from django.conf import settings
from django.contrib.auth.middleware import AuthenticationMiddleware

from .base.views import json_response
from .errors import API_ERROR_CODE, AppError
from .log import lg


# override django AuthenticationMiddleware so that it only works for /admin paths,
# preventing it from writing request.user that are used by our own authenticators (UserAuth)
class AdminAuthMiddleware(AuthenticationMiddleware):
    def process_request(self, request):
        if request.path.startswith('/admin/'):
            return super().process_request(request)
        return


def is_api_path(req):
    return req.path.startswith('/api/')


class ResponseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, e):
        if is_api_path(request):
            return self.process_api_exception(request, e)

    def process_api_exception(self, request, e):
        d = None
        status = 500
        if isinstance(e, pydantic.ValidationError):
            d = {
                'error': f'{e.error_count()} validation error(s)',
                'details': format_pydantic_errors(e.errors()),
                'code': API_ERROR_CODE.PARAMS_INVALID,
            }
            status = 400
        elif isinstance(e, AppError):
            d = {
                'error': str(e),
                'code': e.code,
            }
            status = e.status

        if d is None:
            # if not handled
            if settings.DEBUG is True:
                # if run in DEBUG mode, use default exception handler
                return
            lg.exception(str(e))
            d = {
                'error': str(e),
                'code': API_ERROR_CODE.INTERNAL_ERROR,
            }

        return json_response(d, status=status)


def format_pydantic_errors(errors):
    keys_to_remove = ['input', 'url']
    for i in errors:
        for key in keys_to_remove:
            i.pop(key, None)
    return errors

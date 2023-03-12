from django.http import JsonResponse, HttpRequest
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.views import redirect_to_login as _redirect_to_login
from django.contrib.auth.models import User
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.shortcuts import resolve_url


from urllib.parse import urlparse
import params
from typing import Tuple, Optional

from .log import lg
from .errors import API_ERROR_CODE
from . import errors


def is_api_path(req):
    return req.path.startswith('/api/')


api_code_map = {
    ObjectDoesNotExist: (404, API_ERROR_CODE.RESOURCE_NOT_FOUND),
    params.InvalidParams: (400, API_ERROR_CODE.INVALID_PARAMS),
    errors.OperationNotAllowed: (400, API_ERROR_CODE.OPERATION_NOT_ALLOWED),
    errors.PermissionDenied: (403, API_ERROR_CODE.PERMISSION_DENIED),
    errors.AuthenticationFailed: (401, API_ERROR_CODE.AUTH_FAILED),
    errors.InternalError: (500, API_ERROR_CODE.INTERNAL_ERROR),
}


def get_code_from_map(code_map, e) -> Tuple[Optional[int], Optional[str]]:
    for k, v in code_map.items():
        if isinstance(e, k):
            return v
    return None, None


def parse_invalid_params(e: params.InvalidParams):
    if isinstance(e.errors, list):
        return [{"code": str(x.key), "message": str(x.message)} for x in e.errors]


json_dumps_params = {'ensure_ascii': False}


no_auth_urls = [
    '/login',
    '/logout',
    '/api/login',
    '/api/v1/csrf',
    '/api/v1/login',
    '/api/v1/session',
]

no_auth_url_prefixes = [
    '/admin',
]


def redirect_to_login(request, login_url=None):
    """An enhanced version of django.contrib.auth.views.redirect_to_login."""
    path = request.build_absolute_uri()
    resolved_login_url = resolve_url(login_url or settings.LOGIN_URL)
    # If the login url is the same scheme and net location then just
    # use the path as the "next" url.
    login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
    current_scheme, current_netloc = urlparse(path)[:2]
    if ((not login_scheme or login_scheme == current_scheme) and
            (not login_netloc or login_netloc == current_netloc)):
        path = request.get_full_path()
    return _redirect_to_login(
        path, resolved_login_url, REDIRECT_FIELD_NAME)


class ResponseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        print('init middleware')

    def __call__(self, request: HttpRequest):
        need_auth = True
        if request.path in no_auth_urls:
            need_auth = False
        else:
            for prefix in no_auth_url_prefixes:
                if request.path.startswith(prefix):
                    need_auth = False
                    break

        if need_auth:
            if settings.FAKE_HEADER_AUTH:
                user_id = request.headers.get('X-User-ID')
                if user_id:
                    request.user = User.objects.get(id=int(user_id))
            if not request.user.is_authenticated:
                return redirect_to_login(request)
        return self.get_response(request)

    def process_exception(self, request, e):
        if is_api_path(request):
            return self.process_api_exception(request, e)

    def process_api_exception(self, request, e):
        msg = str(e)
        status, code = get_code_from_map(api_code_map, e)
        if status is None:
            if settings.DEBUG is True:
                raise
            lg.exception(str(e))
            status, code = 500, API_ERROR_CODE.INTERNAL_ERROR
        d = {
            'status': 'error',
            'code': code,
            'message': msg,
        }

        # additional information for some special exceptions
        if isinstance(e, params.InvalidParams):
            errs = parse_invalid_params(e)
            if errs and len(errs) >= 2:
                d['errors'] = errs

        return JsonResponse(d, status=status, json_dumps_params=json_dumps_params)

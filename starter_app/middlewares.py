from django.http import JsonResponse
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

import params
from typing import Tuple, Optional

from .log import app_log
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


class ResponseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        print('init middleware')

    def __call__(self, request):
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
            app_log.exception(str(e))
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


class RequestIdMiddleware:
    def process_request(self, request):
        def add_tag_to_request_scope(header_name):
            request_id = request.META.get("HTTP_X_{}".format(header_name.upper()))
            if request_id:
                with sentry_sdk.configure_scope() as scope:
                    scope.set_tag(header_name.lower(), request_id)

        add_tag_to_request_scope('request_id')
        add_tag_to_request_scope('original_request_id')

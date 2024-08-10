"""
Initialize and configure NinjaAPI instance
"""
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from ninja import NinjaAPI
from ninja.errors import ValidationError
from ninja.renderers import JSONRenderer

from .errors import API_ERROR_CODE, AppError, OperationNotAllowed, is_duplicate_error
from .log import lg


# allow non-ascii characters in json response
JSONRenderer.json_dumps_params = {
    'ensure_ascii': False,
}


ninja = NinjaAPI(renderer=JSONRenderer(), urls_namespace='api')


@ninja.exception_handler(ValidationError)
def handle_validation_error(request, exc: ValidationError):
    # [{'type': 'missing', 'loc': ('query', 'pid'), 'msg': 'Field required'}]
    details = []
    for error in exc.errors:
        details.append({
            'location': error['loc'],
            'message': f'{error["type"]} - {error["msg"]}',
        })
    return ninja.create_response(
        request,
        {
            'error': 'Invalid parameters',
            'details': details,
        },
        status=400)


@ninja.exception_handler(AppError)
def handle_app_error(request, exc: AppError):
    return ninja.create_response(
        request,
        {
            'error': f'{exc}',
            'code': exc.code,
        },
        status=exc.status)


@ninja.exception_handler(ObjectDoesNotExist)
def handle_object_does_not_exist(request, exc: ObjectDoesNotExist):
    return ninja.create_response(
        request,
        {
            'error': f'{exc}',
            'code': API_ERROR_CODE.RESOURCE_NOT_FOUND,
        },
        status=404)


@ninja.exception_handler(IntegrityError)
def handle_integrity_error(request, exc: IntegrityError):
    lg.info(f'caught Integrity Error: {exc}, {exc.args}, {is_duplicate_error(exc)}')
    if is_duplicate_error(exc):
        return ninja.create_response(
            request,
            {
                'error': f'{exc}',
                'code': OperationNotAllowed.code,
            },
            status=OperationNotAllowed.status)
    raise exc

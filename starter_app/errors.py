from django.db import IntegrityError

from .utils.enum import KV, SimpleEnum


class API_ERROR_CODE(SimpleEnum):
    PARAMS_INVALID = KV
    RESOURCE_NOT_FOUND = KV
    AUTH_FAILED = KV
    OPERATION_NOT_ALLOWED = KV
    PERMISSION_DENIED = KV
    FOREIGN_KEY_RESTRICTED = KV
    INTERNAL_ERROR = KV
    UNKNOWN = KV


class AppError(Exception):
    status: int = 500
    code: str = API_ERROR_CODE.UNKNOWN

    def __init__(self, error, status=None, code=None) -> None:
        if status:
            self.status = status
        if code:
            self.code = code
        super().__init__(error)


class ParamsInvalid(AppError):
    status = 400
    code = API_ERROR_CODE.PARAMS_INVALID


class OperationNotAllowed(AppError):
    status = 403
    code = API_ERROR_CODE.OPERATION_NOT_ALLOWED


class PermissionDenied(AppError):
    status = 403
    code = API_ERROR_CODE.PERMISSION_DENIED


class AuthenticationFailed(AppError):
    status = 401
    code = API_ERROR_CODE.AUTH_FAILED


class InternalError(AppError):
    pass


def is_duplicate_error(e):
    if isinstance(e, IntegrityError):
        code = e.args[0]
        if code == 1062:
            return True
    return False

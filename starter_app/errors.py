from .utils.enum import SimpleEnum, KV


class AppError(Exception):
    pass


class OperationNotAllowed(AppError):
    pass


class PermissionDenied(AppError):
    pass


class AuthenticationFailed(AppError):
    pass


class InternalError(AppError):
    pass


class API_ERROR_CODE(SimpleEnum):
    INVALID_PARAMS = KV
    RESOURCE_NOT_FOUND = KV
    AUTH_FAILED = KV
    OPERATION_NOT_ALLOWED = KV
    PERMISSION_DENIED = KV
    INTERNAL_ERROR = KV
    SERVICE_SUSPEND = KV

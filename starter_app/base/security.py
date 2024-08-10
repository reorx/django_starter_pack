from typing import Any, Literal, Optional

from django.http import HttpRequest
from ninja.security.http import HttpAuthBase
from pydantic import BaseModel

from ..errors import AuthenticationFailed
from ..org import auth as org_auth
from ..settings import (
    AUTH_TOKEN_COOKIE_KEY, INTERNAL_AUTH_HEADER, INTERNAL_AUTH_TOKEN
)


AuthType = Literal['user', 'internal']


class AuthResult(BaseModel):
    type: AuthType
    value: Any
    org_id: int|None


class SingleAuthBase(HttpAuthBase):
    is_required: bool
    check_cookie: bool

    def __init__(self, is_required=True, check_cookie=True):
        self.is_required = is_required
        self.check_cookie = check_cookie


class UserAuth(SingleAuthBase):
    def __call__(self, request: HttpRequest) -> Optional[Any]:
        # set request.user, this must be at the beginning to ensure the attribute is set even if the user is not authenticated
        request.user = None
        token = request.META.get('HTTP_AUTHORIZATION')
        if not token and self.check_cookie:
            token = request.COOKIES.get(AUTH_TOKEN_COOKIE_KEY)
        if token:
            try:
                request.user = org_auth.get_user_from_jwt(token)
            except ValueError as e:
                raise AuthenticationFailed(f'Error authenticating user: {e}')

        if not request.user:
            if self.is_required:
                raise AuthenticationFailed('Could not authenticate user')
            return None

        return AuthResult(type='user', value=request.user, org_id=request.user.org_id)


class InternalAuth(SingleAuthBase):
    def __call__(self, request: HttpRequest) -> Optional[Any]:
        # set request.is_internal
        request.is_internal = None
        token = request.headers.get(INTERNAL_AUTH_HEADER)
        if token == INTERNAL_AUTH_TOKEN:
            request.is_internal = True
        elif token:
            raise AuthenticationFailed(f'Error authenticating internal: invalid token')

        if not request.is_internal:
            if self.is_required:
                raise AuthenticationFailed('Could not authenticate internal')
            return None

        return AuthResult(type='internal', value=request.is_internal, org_id=None)


class MultiSourceAuth(HttpAuthBase):
    """This class is a combination of all authenticators (i.e. the SingleAuthBase classes),
    but only one of them will provide the result.

    if any authenticator success, break and return the result.
    """
    auth_types: list[AuthType]
    authenticators: list[SingleAuthBase]

    def __init__(self, auth_types: list[AuthType]):
        self.auth_types = auth_types
        authenticators = []
        # order: user, external_user, internal
        if 'user' in auth_types:
            authenticators.append(UserAuth(is_required=False))
        if 'internal' in auth_types:
            authenticators.append(InternalAuth(is_required=False))
        self.authenticators = authenticators

    def __call__(self, request: HttpRequest) -> Optional[Any]:
        # if any authenticator success, use it as the result, but keep running the rest of the authenticators, so that they can set the request attributes that will be used by the view functions (even if the values are None)
        first_result = None
        for authenticator in self.authenticators:
            result = authenticator(request)
            if result and first_result is None:
                first_result = result

        if first_result:
            return first_result

        raise AuthenticationFailed(f'Could not authenticate {" or ".join(self.auth_types)}')

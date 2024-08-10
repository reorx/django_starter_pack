
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from ninja import Router, Schema
from pydantic import ValidationError

from ...base.security import UserAuth
from ...errors import AuthenticationFailed
from ...settings import AUTH_TOKEN_COOKIE_KEY, AUTH_TOKEN_EXPIRES_IN, AUTH_TOKEN_RESPONSE_HEADER_KEY
from ...types.org import DetailedUserDT
from ...utils.jinja import render
from .. import api, auth


router = Router(auth=None)


class LoginParams(Schema):
    username: str
    password: str


def login_user(params: LoginParams):
    user = api.get_user_by_username(params.username)
    if not user or not user.check_password(params.password):
        raise AuthenticationFailed('invalid username or password')
    api.validate_user_for_login(user)

    token = auth.generate_token(user.pid, AUTH_TOKEN_EXPIRES_IN)
    return user, token


@router.post('/login', response=DetailedUserDT)
def login(request: HttpRequest, params: LoginParams, response: HttpResponse):
    user, token = login_user(params)

    # set header for API use
    response[AUTH_TOKEN_RESPONSE_HEADER_KEY] = token

    # set cookie for browser use
    response.set_cookie(
        AUTH_TOKEN_COOKIE_KEY, token,
        max_age=AUTH_TOKEN_EXPIRES_IN)

    # the same as /user/me for react-query to mutate
    return user


@router.get('/simple_login')
def get_simple_login(request: HttpRequest):
    return render(request, 'simple_login.html', dict(
    ))


@router.post('/simple_login')
def post_simple_login(request: HttpRequest):
    try:
        params = LoginParams.model_validate(request.POST)
    except ValidationError as e:
        print('login error', e)
        return render(request, 'simple_login.html', dict(
            formData=request.POST,
            formErrors={ed['loc'][0]: 'default' for ed in e.errors()},
        ))

    user, token = login_user(params)

    res = HttpResponseRedirect('/')

    # set cookie, no expiration for simple login
    res.set_cookie(
        AUTH_TOKEN_COOKIE_KEY, token)

    return res


user_auth = UserAuth(is_required=True, check_cookie=True)

@router.get('/check_user', auth=None)
def get_check_user(request: HttpRequest, redirect: str = ''):
    try:
        user_auth(request)
    except AuthenticationFailed:
        if redirect:
            return HttpResponseRedirect('/login')
        raise
    return HttpResponse(status=200)

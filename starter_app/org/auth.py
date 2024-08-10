import time
import traceback
from typing import Optional

import jwt

from .. import settings
from .models import User


JWT_ALGORITHM = 'HS256'


def generate_token(user_pid, expires_in):
    secret = settings.AUTH_TOKEN_SECRET
    token = jwt.encode(
        {
            'user_pid': user_pid,
            'exp': int(time.time()) + expires_in,
        },
        secret,
        algorithm=JWT_ALGORITHM,
    )
    return token


def parse_token(token: bytes):
    secret = settings.AUTH_TOKEN_SECRET

    try:
        decoded = jwt.decode(token, secret, algorithms=[JWT_ALGORITHM])
        user_pid = decoded.get('user_pid')
        if not user_pid:
            raise ValueError('invalid token: no user')
        return user_pid
    except jwt.ExpiredSignatureError:
        raise ValueError('token expired')
    except:
        print('*invalid token clause:')
        traceback.print_exc()
        raise ValueError('invalid token')


def get_user_from_jwt(token) -> Optional[User]:
    user_pid = parse_token(token)
    try:
        user = User.objects.select_related('org').get(pid=user_pid)
    except User.DoesNotExist:
        raise ValueError('invalid token: user does not exist')

    return user

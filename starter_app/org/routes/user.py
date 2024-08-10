from typing import List

from django.http import HttpResponse
from ninja import Router, Schema
from pydantic import BaseModel


from ...errors import ParamsInvalid
from ...types.org import DetailedUserDT, UserDT
from .. import api as org_api
from ..models import User


router = Router()


@router.get("/me", response=DetailedUserDT)
def get_me(request):
    return request.user


@router.get("/list", response=list[DetailedUserDT])
def get_list(request):
    qs = User.objects.filter(org_id=request.user.org_id)
    return qs


@router.get("/detail", response=DetailedUserDT)
def get_detail(request, pid: str):
    user = User.objects.select_related('inviter').get(pid=pid, org_id=request.user.org_id)
    return user


class UserCreateParams(Schema):
    username: str|None
    email: str = None
    is_superuser: bool
    group_pids: List[str]


@router.post("/create", response=UserDT)
def post_create(request, params: UserCreateParams):
    if User.objects.filter(org_id=request.user.org_id, username=params.username).exists():
        raise ParamsInvalid("username already exists")

    groups = org_api.get_groups(request.user.org_id, params.group_pids)

    user = org_api.create_user(
        request.user.org, groups, params.username,
        params.email, params.is_superuser)

    return user


class UserUpdateParams(UserCreateParams):
    display_name: str|None
    phone: str|None
    email: str|None
    pid: str
    is_active: bool


@router.post("/update", response=UserDT)
def post_update(request, params: UserUpdateParams):
    user = User.objects.get(pid=params.pid, org_id=request.user.org_id)

    groups = org_api.get_groups(request.user.org_id, params.group_pids)

    org_api.update_user(
        user, groups,  params.display_name, params.phone,
        params.email, params.is_superuser, params.is_active)

    return user


class UserBatchDeleteParams(BaseModel):
    pids: list[str]


@router.post("/batch_delete")
def post_batch_delete(request, params: UserBatchDeleteParams):
    if not params.pids:
        raise ParamsInvalid("pids is empty")

    count = User.objects.filter(
        org_id=request.user.org_id, pid__in=params.pids, is_active=False).count()

    if count != len(params.pids):
        raise ParamsInvalid("invalid pids or user is active")

    admin_count = User.objects.filter(
        org_id=request.user.org_id,  is_superuser=True).exclude(pid__in=params.pids).count()

    if admin_count == 0:
        raise ParamsInvalid("cannot delete all admins")

    User.objects.filter(
        org_id=request.user.org_id, pid__in=params.pids).delete()

    # TODO clear sessions

    return HttpResponse(status=201)

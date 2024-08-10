from typing import List

from django.http import HttpResponse
from ninja import Router, Schema
from pydantic import BaseModel, field_validator

from ...consts.permission import Permission
from ...errors import OperationNotAllowed
from ...types.org import DetailedGroupDT, GroupDT
from .. import api as org_api
from ..models import Group, User


router = Router()


@router.get('list', response=list[GroupDT])
def group_list(request):
    qs = Group.objects.filter(org_id=request.user.org_id)
    return qs


@router.get('detail/{pid}', response=DetailedGroupDT)
def group_detail(request, pid: str):
    return Group.objects.get(pid=pid, org_id=request.user.org_id)


class GroupCreateParams(Schema):
    name: str
    permissions: List[str]
    member_pids: list[str]

    @field_validator('permissions')
    @classmethod
    def validate_permissions(cls, v):
        if not v:
            return []

        # ignore invalid permissions for compatibility of old permissions
        return [i for i in v if i in Permission._values]


@router.post('create', response=DetailedGroupDT)
def group_create(request, params: GroupCreateParams):
    members = list(User.objects.filter(org_id=request.user.org_id, pid__in=params.member_pids))
    group = org_api.create_group(request.user.org, params.permissions, params.name, members)
    return group


class GroupUpdateParams(GroupCreateParams):
    pid: str


@router.post('update', response=DetailedGroupDT)
def group_update(request, params: GroupUpdateParams):
    group = Group.objects.get(pid=params.pid, org_id=request.user.org_id)

    members = list(User.objects.filter(org_id=request.user.org_id, pid__in=params.member_pids))
    group = org_api.update_group(group, params.permissions, params.name, members)
    return group


class GroupDeleteParams(BaseModel):
    pid: str


@router.post('delete')
def group_delete(request, params: GroupDeleteParams):
    group = Group.objects.get(org_id=request.user.org_id, pid=params.pid)

    # make sure the group is not in use
    count = User.objects.filter(org_id=request.user.org_id, groups__pid=params.pid).count()
    if count > 0:
        raise OperationNotAllowed('group is in use')

    group.delete()
    return HttpResponse(status=201)

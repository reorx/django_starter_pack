


from ninja import Schema

from .base import DatetimeToTS


class OrgDT(Schema):
    pid: str
    name: str
    type: int
    is_active: bool
    description: str
    created_at: DatetimeToTS
    updated_at: DatetimeToTS


class GroupDT(Schema):
    pid: str
    name: str
    created_at: DatetimeToTS
    updated_at: DatetimeToTS


class UserDT(Schema):
    pid: str
    display_name: str|None
    username: str|None
    email: str|None
    phone: str|None
    is_active: bool
    is_superuser: bool
    created_at: DatetimeToTS
    updated_at: DatetimeToTS
    inviter_pid: str|None
    inviter_display_name: str|None

    @staticmethod
    def resolve_inviter_pid(obj):
        if obj.inviter:
            return obj.inviter.pid

    @staticmethod
    def resolve_inviter_display_name(obj):
        if obj.inviter:
            return obj.inviter.display_name


class DetailedGroupDT(GroupDT):
    permissions: list[str]
    members: list[UserDT]


class DetailedUserDT(UserDT):
    org: OrgDT
    permissions: list[str]
    groups: list[GroupDT]

    @staticmethod
    def resolve_permissions(obj):
        return obj.get_permissions()

    @staticmethod
    def resolve_groups(obj):
        return obj.get_groups()

from django.core.exceptions import ObjectDoesNotExist
from django.db.transaction import atomic

from ..errors import AuthenticationFailed, OperationNotAllowed
from ..lib.redis import redis
from .models import Group, Org, User


def get_org_id_by_pid(pid):
    redis_key = f'org_pid:{pid}:id'
    v = redis.get(redis_key)
    if v:
        return int(v)
    v = Org.objects.get(pid=pid).id
    redis.set(redis_key, v)
    return v


def get_user_by_username(username):
    try:
        return User.objects.get(username=username)
    except User.DoesNotExist:
        return None


def create_user(org: Org, groups: list[Group], username, email, is_superuser):
    user = User(
        org=org,
        username=username,
        display_name=username,
        email=email,
        is_superuser=is_superuser,
        is_active=False,
    )
    user.save()
    user.groups.set(groups)
    return user


def activate_user(user: User, password):
    user.is_active = True
    user.set_password(password)
    user.save()
    return user


def update_user(user: User, groups: list[Group], display_name, phone, email, is_superuser, is_active):
    with atomic():
        user.groups.set(groups)
        user.display_name= display_name
        user.phone = phone
        user.email = email
        user.is_superuser = is_superuser
        user.is_active = is_active
        user.save()
    return user


def validate_user_for_login(user: User):
    if not user.is_active:
        raise AuthenticationFailed('user inactivated or disabled')
    if not user.org.is_active:
        raise OperationNotAllowed('organization inactivated or disabled')


def create_group(org: Org, permissions: list[str], name, members):
    with atomic():
        group = Group(
            org=org,
            name=name,
            permissions=permissions,
        )
        group.save()
        group.members.set(members)
    return group


def update_group(group: Group, permissions: list[str], name, members):
    with atomic():
        group.permissions = permissions
        group.name = name
        group.save()
        group.members.set(members)
    return group


def get_groups(org_id, group_pids):
    groups = list(Group.objects.filter(org_id=org_id, pid__in=group_pids))
    fetched_pids = {g.pid for g in groups}
    for pid in group_pids:
        if pid not in fetched_pids:
            raise ObjectDoesNotExist(f"Group not found: {pid}")
    return groups

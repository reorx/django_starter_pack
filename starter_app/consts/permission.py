from ..utils.enum import KV, SimpleEnum


class Permission(SimpleEnum):
    ## Top level

    # logicunit
    manage_logicunit = KV

    ## System

    # user
    read_user = KV
    manage_user = KV

    # group
    read_group = KV
    manage_group = KV


class PermissionCategory(SimpleEnum):
    operation = KV
    system = KV


permissions_by_category = {
    PermissionCategory.operation: [
        # scene
        Permission.manage_logicunit,
    ],
    PermissionCategory.system: [
        # user
        Permission.read_user,
        Permission.manage_user,
        # group
        Permission.read_group,
        Permission.manage_group,
    ],
}


def to_ts():
    from ..utils.to_ts_lib import echo_dict, echo_enum, echo_enum_list_dict

    echo_enum(Permission)

    echo_enum(PermissionCategory)

    echo_enum_list_dict('permissions_by_category', permissions_by_category, 'Permission', 'key: string', 'string[]')

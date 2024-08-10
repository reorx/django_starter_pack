export const Permission = {
  manage_logicunit: "manage_logicunit",
  read_user: "read_user",
  manage_user: "manage_user",
  read_group: "read_group",
  manage_group: "manage_group",
} as const;
export const Permission_keys = Object.keys(Permission);
export const Permission_values = Object.values(Permission);

export const PermissionCategory = {
  operation: "operation",
  system: "system",
} as const;
export const PermissionCategory_keys = Object.keys(PermissionCategory);
export const PermissionCategory_values = Object.values(PermissionCategory);

export const permissions_by_category: {[key: string]: string[]} = {
  operation: [Permission.manage_logicunit],
  system: [Permission.read_user, Permission.manage_user, Permission.read_group, Permission.manage_group],
}


/* tslint:disable */
/* eslint-disable */
/**
/* This file was automatically generated from pydantic models by running pydantic2ts.
/* Do not modify it by hand - just update the pydantic models and then re-run the script
*/


export interface DetailedGroupDT {
  pid: string;
  name: string;
  created_at: number;
  updated_at: number;
  permissions: string[];
  members: UserDT[];
}

export interface UserDT {
  pid: string;
  display_name: string | null;
  username: string | null;
  email: string | null;
  phone: string | null;
  is_active: boolean;
  is_superuser: boolean;
  created_at: number;
  updated_at: number;
  inviter_pid: string | null;
  inviter_display_name: string | null;
}

export interface DetailedUserDT {
  pid: string;
  display_name: string | null;
  username: string | null;
  email: string | null;
  phone: string | null;
  is_active: boolean;
  is_superuser: boolean;
  created_at: number;
  updated_at: number;
  inviter_pid: string | null;
  inviter_display_name: string | null;
  org: OrgDT;
  permissions: string[];
  groups: GroupDT[];
}

export interface OrgDT {
  pid: string;
  name: string;
  type: number;
  is_active: boolean;
  description: string;
  created_at: number;
  updated_at: number;
}

export interface GroupDT {
  pid: string;
  name: string;
  created_at: number;
  updated_at: number;
}

export interface Schema {}

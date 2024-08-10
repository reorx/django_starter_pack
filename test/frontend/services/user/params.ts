/* tslint:disable */
/* eslint-disable */
/**
/* This file was automatically generated from pydantic models by running pydantic2ts.
/* Do not modify it by hand - just update the pydantic models and then re-run the script
*/


export interface UserBatchDeleteParams {
  pids: string[];
}

export interface UserCreateParams {
  username: string | null;
  email?: string;
  is_superuser: boolean;
  group_pids: string[];
}

export interface UserUpdateParams {
  username: string | null;
  email: string | null;
  is_superuser: boolean;
  group_pids: string[];
  display_name: string | null;
  phone: string | null;
  pid: string;
  is_active: boolean;
}

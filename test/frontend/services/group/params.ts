/* tslint:disable */
/* eslint-disable */
/**
/* This file was automatically generated from pydantic models by running pydantic2ts.
/* Do not modify it by hand - just update the pydantic models and then re-run the script
*/


export interface GroupCreateParams {
  name: string;
  permissions: string[];
  member_pids: string[];
}

export interface GroupDeleteParams {
  pid: string;
}

export interface GroupUpdateParams {
  name: string;
  permissions: string[];
  member_pids: string[];
  pid: string;
}

# coding: utf-8

from __future__ import absolute_import

import functools
from django.db import close_old_connections, connections, DEFAULT_DB_ALIAS
from django.db.migrations.executor import MigrationExecutor


def close_connection_after_call(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        result = f(*args, **kwargs)
        close_old_connections()
        return result
    return wrapper


def is_db_synchronized(database=DEFAULT_DB_ALIAS, exclude_apps=[]):
    connection = connections[database]
    connection.prepare_database()
    executor = MigrationExecutor(connection)
    targets = executor.loader.graph.leaf_nodes()

    plan = []
    for plan_item in executor.migration_plan(targets):
        if plan_item[0].app_label in exclude_apps:
            continue
        plan.append(plan_item)
    if plan:
        print('has migration plan: {}'.format(plan))
        return False
    return True


def exit_if_db_not_synchronized(**kwargs):
    if not is_db_synchronized(**kwargs):
        raise SystemExit('exit because db migrations is not synchronized')

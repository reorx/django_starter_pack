# coding: utf-8
from __future__ import print_function
from starter_app.utils import setup_django

setup_django('starter_app')

from django.db import connection
from django.conf import settings
import pprint


def execute_print(cursor, sql):
    cursor.execute(sql)
    print(sql)
    for i in cursor.fetchall():
        print('  {}'.format(i))


def main():
    print('DATABASE conf:')
    pprint.pprint(settings.DATABASES['default'])
    with connection.cursor() as cur:
        sqls = [
            r"SELECT USER();",
            r"SELECT DATABASE();",
            r"SHOW VARIABLES LIKE 'character%';",
            r"SHOW VARIABLES LIKE 'sql_mode';",
            r"SHOW VARIABLES LIKE 'default_storage_engine';",
        ]
        for sql in sqls:
            execute_print(cur, sql)


if __name__ == '__main__':
    main()

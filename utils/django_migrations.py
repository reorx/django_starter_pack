import logging
from django.contrib.contenttypes.models import ContentType


class DeleteModelMigrator(object):
    def __init__(self, model_name):
        self.model_name = model_name
        self.permissions = []

    def delete_permission(self, apps, schema_editor):
        from django.contrib.auth.models import Permission

        # We get the model from the versioned app registry;
        # if we directly import it, it'll be the wrong version
        try:
            ct = ContentType.objects.get(app_label='msscore', model=self.model_name)
        except ContentType.DoesNotExist:
            print("msscore %s not found, permission fix pass", self.model_name)
        else:
            db_alias = schema_editor.connection.alias
            self.permissions = list(Permission.objects.using(db_alias).filter(content_type=ct).values())
            Permission.objects.using(db_alias).filter(
                name__in=[p['name'] for p in self.permissions]).delete()

    def recover_permission(self, apps, schema_editor):
        from django.contrib.auth.models import Permission

        # forwards_func() creates two Country instances,
        # so reverse_func() should delete them.
        # ct = ContentType.objects.get(app_label='msscore', model='WireBankcard')
        # db_alias = schema_editor.connection.alias
        if len(self.permissions):
            Permission.objects.bulk_create([Permission(**d) for d in self.permissions])

    def delete_admin_log(self, apps, schema_editor):
        from django.contrib.admin.models import LogEntry

        try:
            ct = ContentType.objects.get(app_label='msscore', model=self.model_name)
        except ContentType.DoesNotExist:
            print("msscore %s not found, permission fix pass", self.model_name)
        else:
            qs = LogEntry.objects.filter(content_type=ct)
            logging.info('deleting %s admin logs', qs.count())
            qs.delete()


class DisableMigrations(object):
    """
    avoid migration error for multiple dbs and speed tests.
    django will create tables according to models if can't
    find any migrations for all apps.

    https://docs.djangoproject.com/zh-hans/2.1/ref/settings/#std:setting-MIGRATION_MODULES
    """

    def __contains__(self, item):
        return True

    def __getitem__(self, key):
        return None

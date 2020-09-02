from django.apps import AppConfig as BaseAppConfig
from importlib import import_module


SUBAPPS = [
    'contact',
]


class AppConfig(BaseAppConfig):
    name = 'starter_app'

    # WARN not compatible for django < 1.11
    def import_models(self):
        self.models = self.apps.all_models[self.label]

        models_module = None
        for i in SUBAPPS:
            models_module_name = '{}.{}.models'.format(self.name, i)
            models_module = import_module(models_module_name)

        self.models_module = models_module

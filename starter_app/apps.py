from importlib import import_module

from django.apps import AppConfig as BaseAppConfig


SUBAPPS = [
    'subapp',
    'org',
]


class AppConfig(BaseAppConfig):
    name = 'starter_app'

    # WARN not compatible for django < 1.11
    def import_models(self):
        self.models = self.apps.all_models[self.label]

        models_module = None
        for i in SUBAPPS:
            models_module = import_module(f'{self.name}.{i}.models')

        self.models_module = models_module

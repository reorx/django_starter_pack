from importlib import import_module

from django.conf import settings
from django.contrib import admin

from .apps import SUBAPPS, AppConfig


for i in SUBAPPS:
    import_module(f'.{i}.admin', package=AppConfig.name)


admin.site.site_header = settings.ADMIN_TITLE + ' Admin'

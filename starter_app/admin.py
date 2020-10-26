from django.contrib import admin
from django.conf import settings
from .contact import admin as _


admin.site.site_header = settings.ADMIN_TITLE + ' Admin'

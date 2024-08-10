from django.db import models

from ..utils.hash import gen_uuid


class PublicIdMixin(models.Model):
    # not using UUIDField because it returns uuid.UUID instance
    pid = models.CharField(max_length=36, default=gen_uuid, unique=True)

    class Meta:
        abstract = True


class DatetimeMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

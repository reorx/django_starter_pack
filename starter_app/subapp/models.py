from django.db import models
from django.db.models import CharField, DateTimeField, TextField


class LogicUnit(models.Model):
    email = CharField(max_length=64, unique=True)
    company = CharField(max_length=64)
    note = TextField(blank=True)

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        db_table = 'logic_unit'

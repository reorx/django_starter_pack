from django.db.models import CharField

from ..base.models import DatetimeMixin


class LogicUnit(DatetimeMixin):
    name = CharField(max_length=64, unique=True)

    class Meta:
        db_table = 'logic_unit'

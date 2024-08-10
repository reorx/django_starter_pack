from .models import LogicUnit


def create_logic_unit() -> LogicUnit:
    u = LogicUnit.objects.create()
    return u

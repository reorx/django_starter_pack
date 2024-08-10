from ninja import Router

from ...types.org import OrgDT
from ..models import Org


router = Router()


@router.get('/list', response=list[OrgDT])
def get_list(request):
    qs = Org.objects.all()
    return qs


@router.get('/info', response=OrgDT)
def get_info(request, pid: str):
    return Org.objects.get(pid=pid)

import math
import params
from params import InvalidParams
from django.db.models import Q
from functools import reduce


class PaginatorParams(params.ParamSet):
    page = params.IntegerField(default=1, null=False)
    limit = params.IntegerField(default=20, min=1, max=500, null=False)
    sort = params.WordField(
        choices=[
            'created_at', 'updated_at'
        ], default='updated_at')
    order = params.WordField(
        choices=[
            'asc', 'desc'
        ],
        default='desc')


def paginate_queryset(qs, page, limit, sort=None, order='asc'):
    """
    paginating:
    'data': data,
    'count': count,
    'limit': limit,
    'index': index,
    'pages': math.ceil(count / float(limit)),
    """
    if sort is not None:
        order_by_prefix = '-' if order == 'desc' else ''
        order_by_key = sort
        order_by_arg = order_by_prefix + order_by_key
        qs = qs.order_by(order_by_arg)

    if not isinstance(page, int) or not isinstance(limit, int) or page <= 0:
        raise InvalidParams("index or max argument overflow")

    count = qs.count()
    offset = limit * (page - 1)

    pages = int(math.ceil(count / float(limit)))
    rqs = qs[offset:offset + limit]
    d = {
        'data': rqs,
        'count': count,
        'limit': limit,
        'page': page,
        'pages': pages,
    }
    return d


def paginate_list(l, page, limit):
    """
    paginating:
    'data': data,
    'count': count,
    'limit': limit,
    'index': index,
    'pages': math.ceil(count / float(limit)),
    """
    count = len(l)
    offset = limit * (page - 1)

    if page <= 0:
        raise InvalidParams("index or max argument overflow")

    pages = int(math.ceil(count / float(limit)))
    rqs = l[offset:offset + limit]
    d = {
        'data': rqs,
        'count': count,
        'limit': limit,
        'page': page,
        'pages': pages,
    }
    return d


def qs_search(qs, and_kvs=None, or_kvs=None):
    if and_kvs and or_kvs:
        raise ValueError('and_kvs and or_kvs are mutually exclusive')
    if not and_kvs and not or_kvs:
        raise ValueError('either and_kvs or or_kvs must be passed')
    if and_kvs:
        kvs = and_kvs
    else:
        kvs = or_kvs
    qobjs = []
    for k, v in kvs:
        qobjs.append(Q(**{k + '__icontains': v}))
    if and_kvs:
        # objects.filter(Q1, Q2, ...)
        qs = qs.filter(*qobjs)
    else:
        # objects.filter(Q1 | Q2 | ...)
        qs = qs.filter(reduce(lambda x, y: x | y, qobjs))
    return qs

import datetime
from json import JSONEncoder

from django.http import JsonResponse
from pydantic import BaseModel

from ..utils.time import TIME_FORMATS, datetime2ts, format_time


class CustomJSONEncoder(JSONEncoder):
    """
    JSONEncoder subclass that knows how to encode date/time, enum, pydantic model and other things
    """
    def default(self, o):
        # See "Date Time String Format" in the ECMA-262 specification.
        # the order of datetime, date matter due to datetime being subclass of date

        if isinstance(o, datetime.datetime):
            # Assume this object has `tzinfo` or is a UTC time
            return datetime2ts(o)
        if isinstance(o, datetime.date):
            return format_time(o, TIME_FORMATS.YMD)
        if isinstance(o, BaseModel):
            return o.model_dump()
        else:
            return super().default(o)


def json_response(
    data,
    status=200,
    headers=None,
    encoder=CustomJSONEncoder,
    json_dumps_params=None,
    **kwargs,
):
    if json_dumps_params is None:
        json_dumps_params = {}
    json_dumps_params.update({"ensure_ascii": False})

    return JsonResponse(
        data,
        encoder=encoder,
        status=status,
        headers=headers,
        json_dumps_params=json_dumps_params,
        safe=False,
        **kwargs
    )


def queryset_to_dict(qs):
    # convert django <QueryDict> to dict, when <QueryDict>
    # is like <QueryDict {'a': ['1'], 'b': ['x', 'y']}>,
    # iteritems will make 'a' return '1', 'b' return 'y',
    # we should convert it to a normal dict so that 'b' keeps
    # ['x', 'y']
    raw = {}
    for k, v in qs.items():
        if not v:
            continue
        if len(v) == 1:
            raw[k] = v[0]
        else:
            raw[k] = v
    return raw

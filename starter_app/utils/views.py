import json
import logging
from copy import deepcopy
from datetime import datetime, timedelta

from django.http import HttpResponse
from django.views.generic import View
import params
from params import InvalidParams

from ..errors import AuthenticationFailed
from .models_formatter import ModelJSONEncoder
from .models_paginator import PaginatorParams


lg = logging.getLogger('starter_app.views')


class BaseAuthMixin(object):
    def must_get_auth_token(self, request):
        t = request.META.get('HTTP_AUTHORIZATION')
        if not t:
            raise AuthenticationFailed('could not get Authorization header')
        return t


def delete_keys(data: dict, keys):
    if not data:
        return data
    assert isinstance(data, dict)
    for k in keys:
        if k in data:
            del data[k]
    return data


class JSONView(BaseAuthMixin, View):
    @property
    def json(self):
        if not hasattr(self, '_json'):
            try:
                self._json = json.loads(self.request.body)
            except Exception as e:
                raise InvalidParams('could not parse body as json: {}'.format(e))
        return self._json

    @property
    def json_str(self):
        if not hasattr(self, '_json_str'):
            self._json_str = json.dumps(self.json)
        return self._json_str

    @staticmethod
    def json_response(
        data,
        status=200,
        encoder=ModelJSONEncoder,
        json_dumps_params=None,
        as_root_data=False,
        **kwargs,
    ):
        if as_root_data:
            data = {'data': data}
        if not isinstance(data, str):
            if json_dumps_params is None:
                json_dumps_params = {}
            json_dumps_params.update({"ensure_ascii": False})
            data = json.dumps(data, cls=encoder, **json_dumps_params)
        return HttpResponse(
            content=data, status=status, content_type='application/json', **kwargs
        )

    def error_response(self, error, status, code=0):
        d = {'status': 'error', 'code': code, 'message': error}
        return self.json_response(d, status)

    @staticmethod
    def remove_paginator_keys(data):
        data = deepcopy(data)
        delete_keys(data, list(PaginatorParams.keys()))
        return data

    def process_start_end_date(self, data, field_names=("updated_at", "created_at")):
        data = self.remove_paginator_keys(data)
        if not isinstance(field_names, (list, tuple)):
            field_names = [field_names]

        for name in field_names:
            start = data.pop("{}_start".format(name), None)
            end = data.pop("{}_end".format(name), None)
            if start:
                # start = make_aware_utc(start)
                assert isinstance(start, datetime)
                data["{}__gte".format(name)] = start
            if end:
                # end = make_aware_utc(end)
                assert isinstance(end, datetime)
                data["{}__lt".format(name)] = end + timedelta(days=1)
        return data

    def get_client_ip(self):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip

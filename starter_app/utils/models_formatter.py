# coding: utf-8

import datetime
from json import JSONEncoder

import arrow
from django.db.models import QuerySet, Model
from django.forms import model_to_dict
import six


# ISO 8601
# https://www.w3.org/TR/NOTE-datetime
# http://crsmithdev.com/arrow/#tokens

TIME_FORMAT = 'YYYY-MM-DDTHH:mm:ss.SSSZZ'
DATE_FORMAT = '%Y-%m-%d'
DATE_TIME_WITH_TIMEZONE = "%Y-%m-%dT%H:%M:%S%z"


class ModelJSONEncoder(JSONEncoder):
    """
    JSONEncoder subclass that knows how to encode date/time, enum, django model and other things
    """
    def default(self, o):
        # See "Date Time String Format" in the ECMA-262 specification.
        # the order of datetime, date matter due to datetime being subclass of date

        if isinstance(o, datetime.datetime):
            # Assume this object has `tzinfo` or is a UTC time
            return arrow.get(o).format(TIME_FORMAT)
        if isinstance(o, datetime.date):
            return o.strftime(DATE_FORMAT)
        if isinstance(o, QuerySet):
            return list(o)
        if isinstance(o, Model):
            return model_to_dict(o)
        else:
            return super(ModelJSONEncoder, self).default(o)


def get_encoder_by_exclude_keys(ks):
    class Encoder(ModelJSONEncoder):
        def default(self, o):
            v = super().default(o)
            if isinstance(o, Model):
                for k in ks:
                    del v[k]
            return v

    return Encoder


class ArbitraryJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            # Assume this object has `tzinfo` or is a UTC time
            return arrow.get(o).format(TIME_FORMAT)
        if isinstance(o, datetime.date):
            return o.strftime(DATE_FORMAT)
        if isinstance(o, set):
            return list(o)
        try:
            return str(o)
        except Exception:
            return repr(o)


def make_model_encoder(model_class, func):
    class CustomEncoder(ModelJSONEncoder):
        def default(self, o):
            if isinstance(o, model_class):
                return func(o)
            return super(CustomEncoder, self).default(o)

    return CustomEncoder


def make_models_encoder(model_func_tuple_list):
    class CustomEncoder(ModelJSONEncoder):
        def default(self, o):
            for model_class, func in model_func_tuple_list:
                if isinstance(o, model_class):
                    return func(o)
            return super(CustomEncoder, self).default(o)
    return CustomEncoder


def make_model_formatter(formats, func=None, optional_key_funcs=None):
    """

    :param formats:
    :param func:
    :param optional_key_funcs: {key1: func1, key2: func2}
    :return:
    """
    keymap = {}
    funcmap = {}
    for i in formats:
        if isinstance(i, tuple):
            field = i[1]
            if isinstance(field, six.string_types):
                keymap[i[0]] = field
            else:
                funcmap[i[0]] = field
        else:
            keymap[i] = i

    def _formatter(o, **kwargs):
        d = {}
        for k, v in keymap.items():
            vv = getattr(o, v)
            if optional_key_funcs and v in optional_key_funcs and optional_key_funcs[v](vv):
                continue
            d[k] = vv

        for k, v in funcmap.items():
            vv = v(o)
            if optional_key_funcs and v in optional_key_funcs and optional_key_funcs[v](vv):
                continue
            d[k] = vv

        if func is not None:
            func(d, o)
        return d

    return _formatter


def make_dict_formatter(formats, func=None, ignore_keyerror=False):
    keymap = {}
    for i in formats:
        keymap[i] = i

    def _formatter(d, **kwargs):
        r = {}
        for k, v in keymap.items():
            d_value = d.get(v)
            if ignore_keyerror and d_value is None:
                r[k] = d_value
            else:
                r[k] = d[v]

        if func is not None:
            func(d, d)
        return r

    return _formatter


def model_to_str(o, exclude_fields=None):
    if exclude_fields is None:
        exclude_fields = []
    model_name = o.__class__.__name__
    d = model_to_dict(o)
    kvs = []
    for k, v in list(d.items()):
        if k in exclude_fields:
            continue
        kvs.append('{}={}'.format(k, v))
    return '{}<{}>'.format(
        model_name, ' '.join(kvs),
    )

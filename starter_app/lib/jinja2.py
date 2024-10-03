from urllib.parse import urlencode

import arrow
from django.templatetags.static import static
from django.urls import reverse
from django.utils.timezone import localtime
from jinja2 import Environment


filters = {}
context = {}


def environment(**options):
    env = Environment(**options)

    env.globals.update(
        {
            "static": static,
        }
    )
    env.globals.update(context)
    env.filters.update(filters)
    return env


def register_filter(f):
    filters[f.__name__] = f
    return f


def register_context(f):
    context[f.__name__] = f
    return f


@register_context
def url(name, *args):
    return reverse(name, args=args)


@register_context
def url_with_params(name, *args, params=None):
    url = reverse(name, args=args)
    if params:
        url += '?' + urlencode(params)
    return url


@register_context
def ternary(value, true_val, false_val):
    return true_val if value else false_val


iso_time_format = '%Y-%m-%d %H:%M:%S%z'


@register_filter
@register_context
def iso_time(t):
    if not t:
        return '-'
    return localtime(t).strftime(iso_time_format)


@register_context
def relative_to_now(t):
    return arrow.get(t).humanize()


@register_context
def encode_params_with_page(params, page=None):
    newparams = dict(params)
    if page is not None:
        newparams['page'] = page
    return urlencode(newparams, True)

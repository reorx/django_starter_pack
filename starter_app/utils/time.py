
import datetime
from unittest import mock

import arrow
from dateutil.tz import gettz
# not directly import now to prevent caching it in the module, which may cause mock not working
from django.utils import timezone as django_timezone

from ..settings import TIME_ZONE


def datetime_now():
    """The only entrance to get current datetime in the whole project.

    NOTE the result has no timezone info, it is only timezone aware,
    meaning that the timestamp is correct, but the hours and minutes
    are not reflecting the correct values in timezone.

    To get the datetime with settings.TIME_ZONE, use arrow_now() or datetime_now_tz().
    """
    return django_timezone.now()


def utc(d: datetime.datetime):
    """
    convert a datetime to UTC timezone
    """
    return d.astimezone(datetime.timezone.utc)


def utc_day_time(day: str, shift_days: int = 0):
    result = arrow.get(day, 'YYYY-MM-DD', tzinfo=gettz(TIME_ZONE))
    if shift_days:
        result = result.shift(days=shift_days)
    return utc(result.datetime)

# arrow #

def arrow_now():
    return arrow.get(datetime_now()).to(TIME_ZONE)


def arrow_date_only(dt):
    return arrow.get(dt.date(), TIME_ZONE)


def datetime_now_tz():
    return arrow_now().datetime


class TIME_FORMATS:
    YMDHMS = 'YYYY-MM-DD HH:mm:ss'
    YMDHMS_TZ = 'YYYY-MM-DD HH:mm:ss ZZ'
    ZH_YMDHMS = 'YYYY年M月D日 HH:mm:ss'
    YMD_HMS = 'YYYYMMDD_HHmmss'
    YMD = 'YYYYMMDD'
    HMS = 'HHmmss'


def format_time(dt, format=TIME_FORMATS.YMDHMS):
    return arrow.get(dt).to(TIME_ZONE).format(format)


def format_now(format=TIME_FORMATS.YMDHMS):
    return format_time(datetime_now(), format)


def ts2datetime(ts):
    return arrow.get(ts).to(TIME_ZONE).datetime

def tsshift(ts, seconds=None):
    return arrow.get(ts).shift(seconds=seconds).timestamp

def datetime_now_shift(**shift_kwargs):
    return arrow_now().shift(**shift_kwargs).datetime

def datetime2ts(dt):
    """datetime to 13 digits timestamp"""
    return int(dt.timestamp() * 1000)


def ts10_now():
    return int(datetime_now().timestamp())


def get_ymd_and_hms() -> tuple[str, str]:
    """get YMD and HMS string of now, used for file name etc."""
    now = datetime_now()
    return format_time(now, TIME_FORMATS.YMD), format_time(now, TIME_FORMATS.HMS)


def humanize_seconds(n: int):
    s = ''
    min = n // 60
    if min:
        s += f'{min}分钟'
    sec = n % 60
    if sec:
        s += f'{sec}秒'
    return s


# testing #

def mock_now(now=None, **shift_kwargs):
    if now is None:
        now = datetime_now()
    elif isinstance(now, str):
        now = arrow.get(now).datetime
    elif not isinstance(now, datetime.datetime):
        raise ValueError('now must be a string or datetime')

    if shift_kwargs:
        now = arrow.get(now).shift(**shift_kwargs).datetime
    return mock.patch('django.utils.timezone.now', mock.Mock(return_value=now))

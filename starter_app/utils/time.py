import arrow
from ..settings import TIME_ZONE


def format_time(dt):
    return arrow.get(dt).to(TIME_ZONE).format('YYYY-MM-DD HH:mm:ss')


def format_time_tz(dt):
    return arrow.get(dt).to(TIME_ZONE).format('YYYY-MM-DD HH:mm:ss ZZ')


def format_time_zh(dt):
    return arrow.get(dt).to(TIME_ZONE).format('YYYY年M月D日 HH:mm:ss')

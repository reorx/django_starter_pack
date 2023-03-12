import datetime
import arrow
from ..settings import TIME_ZONE

# arrow #

def format_time(dt):
    return arrow.get(dt).to(TIME_ZONE).format('YYYY-MM-DD HH:mm:ss')


def format_time_tz(dt):
    return arrow.get(dt).to(TIME_ZONE).format('YYYY-MM-DD HH:mm:ss ZZ')


def format_time_zh(dt):
    return arrow.get(dt).to(TIME_ZONE).format('YYYY年M月D日 HH:mm:ss')


# datetime #

tz = datetime.timezone(datetime.timedelta(hours=8))


def get_now():
    """
    NOTE this function is not effected by TZ environment
    """
    now = datetime.datetime.now(tz=tz)
    return now


def get_today_str(fmt='%Y-%m-%d'):
    return get_now().strftime(fmt)


def get_utc_now_str():
    return datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

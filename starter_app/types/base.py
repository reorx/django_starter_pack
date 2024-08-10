from datetime import date
import re
from typing import Annotated

from pydantic import AfterValidator, BeforeValidator

from ..utils.time import datetime2ts


def validate_datetime2ts(value):
    if isinstance(value, int):
        return value
    return datetime2ts(value)

DatetimeToTS = Annotated[int, BeforeValidator(validate_datetime2ts)]


password_regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+{}\[\]:;<>,.?~\\/-]).{8,16}$"

def validate_password(value):
    assert re.match(password_regex, value), 'password does not meet requirements'
    return value

Password = Annotated[str, AfterValidator(validate_password)]

def validate_date2str(value):
    if isinstance(value, date):
        return value.strftime('%Y-%m-%d')
    return ''

DateToStr = Annotated[str, BeforeValidator(validate_date2str)]
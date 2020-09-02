import json
import os
import re
from collections import OrderedDict, deque

import jsonschema.exceptions
from django.conf import settings
from jsonschema import Draft4Validator, FormatChecker, Draft6Validator
from params import InvalidParams
from params.core import FieldErrorInfo


# store validators globally
_validators = {}


# see https://stackoverflow.com/questions/26063899/python-version-3-4-does-not-support-a-ur-prefix
_regex_ascii_printable = r'^[\u0020-\u007E]+$'  # type: Text
regex_ascii_printable = re.compile(_regex_ascii_printable)


@FormatChecker.cls_checks('ascii_printable')
def check_format_ascii_printable(v):
    if not isinstance(v, str):
        return True
    if regex_ascii_printable.match(str(v)):
        return True
    return False


format_checker = FormatChecker()


def get_validator(schema_name, draft_version=4, relative='schemas/dist', schema=None):
    if schema_name not in _validators:
        if schema is None:
            schema = get_schema(schema_name, relative=relative)
        return make_validator(schema_name, schema, draft_version)
    return _validators[schema_name]


def has_validator(name):
    return name in _validators


def get_schema(schema_name, relative='schemas/dist'):
    project_relative = get_relative_searcher()
    schema_dir = project_relative.join(relative)
    filepath = os.path.join(schema_dir, schema_name + '.json')
    with open(filepath, 'r') as f:
        content = f.read()
    schema = json.loads(content, object_pairs_hook=OrderedDict)
    return schema


def format_path_queue(schema_path: deque) -> str:
    return '.'.join(str(y) for y in schema_path)


def make_validator(schema_name, schema, draft_version=4):
    supported_draft_versions = [4, 6]
    if draft_version not in supported_draft_versions:
        raise ValueError('invalid draft_version.')

    def validator(data, raise_params_error):
        try:
            if draft_version == 4:
                Draft4Validator(schema, format_checker=format_checker).validate(data)
            elif draft_version == 6:
                Draft6Validator(schema, format_checker=format_checker).validate(data)
        except jsonschema.exceptions.ValidationError as e:
            if settings.DEBUG:
                print(json.dumps(data, ensure_ascii=False, indent=2))
            if raise_params_error:
                if e.context:
                    errs = [
                        FieldErrorInfo(
                            '{}:{}'.format(format_path_queue(x.absolute_path), format_path_queue(x.schema_path)),
                            x.message
                        ) for x in e.context
                    ]
                    raise InvalidParams(errs)
                else:
                    error_path = format_path_queue(e.absolute_path)
                    if error_path:
                        msg = '{}: {}'.format(error_path, e.message)
                    else:
                        msg = e.message
                    raise InvalidParams(msg)
            else:
                raise
        return data

    _validators[schema_name] = validator
    return _validators[schema_name]


def validate_value(field, value, convert=True):
    try:
        return field.validate(value, convert=convert)
    except ValueError as e:
        raise InvalidParams(str(e))

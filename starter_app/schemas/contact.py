from ..utils.json_schema import get_validator


contact_schema = {
    '$schema': 'http://json-schema.org/draft-04/schema#',
    'version': 1,
    'type': 'object',
    'additionalProperties': False,
    'required': [
        'email',
        'company',
    ],
    'properties': {
        'email': {
            'type': 'string'
        },
        'company': {
            'type': 'string',
        },
        'note': {
            'type': 'string',
        }
    }
}

# add extra validation in this function
def validate_contact_schema(data):
    va = get_validator('contact', schema=contact_schema)
    return va(data, True)

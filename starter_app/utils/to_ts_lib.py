def echo_value(v):
    if isinstance(v, str):
        return f'"{v}"'
    return str(v)


def echo_enum(enum):
    lines = '\n'.join(f'  {k}: {echo_value(v)},' for k, v in enum.items())
    s = f"""\
export const {enum.__name__} = {{
{lines}
}} as const;
export const {enum.__name__}_keys = Object.keys({enum.__name__});
export const {enum.__name__}_values = Object.values({enum.__name__});
"""
    print(s)


def echo_dict(name, d, key_type='key: string', value_type='string'):
    lines = '\n'.join(f'  {k}: {echo_value(v)},' for k, v in d.items())
    s = f"""\
export const {name}: {{[{key_type}]: {value_type}}} = {{
{lines}
}}
"""
    print(s)

def echo_enum_list_dict(name, d, enum_name, key_type='key: string', value_type='string'):
    def enum_list_to_str(enum_list):
        return '[' + ', '.join(f'{enum_name}.{i}' for i in enum_list) + ']'

    lines = '\n'.join(f'  {k}: {enum_list_to_str(v)},' for k, v in d.items())
    s = f"""\
export const {name}: {{[{key_type}]: {value_type}}} = {{
{lines}
}}
"""
    print(s)

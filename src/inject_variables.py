from colorama import init, Fore
from datetime import date
import random
import json
import traceback
from string import Formatter
# def inject(script, data={}):
#     if isinstance(script, dict):
#         for (key, value) in script.items():
#             if isinstance(value, str):
#                 if '{{ ' in value and ' }}' in value:
#                     try:
#                         new_value = value.replace('{{ ','').replace(' }}','')
#                         new_value = eval(new_value, dict( random=random, data=date, **data,))
#                         script[key] = new_value
#                     except Exception as e:
#                         init(autoreset=True)
#                         print(Fore.RED + 'couldn\'t replace {}},\n{}'.format(value, e))
#             else:
#                 inject(script[key], data)
#     else:
#         return

# class MissingAttrHandler(str):
#     def __init__(self, format):
#         self.format = format
#
#     def __getattr__(self, attr):
#         return type(self)('{}.{}'.format(self.format, attr))
#
#     def __repr__(self):
#         return MissingAttrHandler(self.format + '!r}')
#
#     def __str__(self):
#         return MissingAttrHandler(self.format + '!s}')
#
#     def __format__(self, format):
#         if self.format.endswith('}'):
#             self.format = self.format[:-1]
#         return '{}:{}}}'.format(self.format, format)
#
# class safedotdict(dict):
#     """dot.notation access to dictionary attributes"""
#     def __getattr__(self, attr):
#         print('called')
#         val = dict.__getitem__(self, attr)
#         if isinstance(val, dict):
#             return safedotdict(**val)
#         else:
#             return val
#     def __setattr__(self, attr):
#         print('called')
#         val = dict.__setitem__(self, attr)
#         if isinstance(val, dict):
#             return safedotdict(**val)
#         else:
#             return val
#     __delattr__ = dict.__delitem__
#     def __missing__(self, key):
#         return '{' + safedotdict(**eval(key)) + '}'




def get_field_value(field_name, mapping):
    try:
        def recursive_get(field_name, mapping):

                if '.' not in field_name:
                    return mapping[field_name], True
                else:
                    *attrs, = field_name.split('.')
                    return recursive_get(".".join(attrs[1:]), mapping[attrs[0]])
        return recursive_get(field_name, mapping)

    except Exception as e:
        # traceback.print_exc()
        return field_name, False




def str_format_map(format_string, mapping):
    f = Formatter()
    parsed = f.parse(format_string)
    output = []
    for literal_text, field_name, format_spec, conversion in parsed:
        conversion = '!' + conversion if conversion is not None else ''
        format_spec = ':' + format_spec if format_spec else ''
        if field_name is not None:
            field_value, found = get_field_value(field_name, mapping)
            if not found:
                text = '{{{}{}{}}}'.format(field_value,
                                           conversion,
                                           format_spec)
            else:
                format_string = '{{{}{}}}'.format(conversion, format_spec)
                text = format_string.format(field_value)
        output.append(literal_text + text)
        text = ''
    return ''.join(output)


def inject(script, data={}):
    variables = data #safedotdict(**data)
    if isinstance(script, dict):
        for (key, value) in script.items():
            if isinstance(value, str):
                if '{' in value and '}' in value:
                    try:
                        new_value = str_format_map(value, variables)
                        script[key] = new_value
                    except Exception as e:
                        init(autoreset=True)
                        print(Fore.RED + 'error in {},\n{}'.format(value, e))
            else:
                inject(script[key], data)
    else:
        return

# 
# if __name__ == '__main__':
#     stuff = dict(
#         a=dict(
#             b=1,
#             c='{a.b}'
#         )
#     )
#     inject(stuff, data=dict(
#         a=dict(
#             b=dict(
#                 c=2
#                 )
#             )
#         )
#     )
#     print(json.dumps(stuff, indent=4))

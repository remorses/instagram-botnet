from colorama import init, Fore
import os
import operator
from string import Formatter
import random
from .support import merge, dotdict
import funcy

def get_field_value(field_name, mapping):
    try:
        def recursive_get(field_name, mapping):

                if '.' not in field_name:
                    return mapping[field_name], True
                else:
                    *attrs, = field_name.split('.')
                    return recursive_get(".".join(attrs[1:]), mapping[attrs[0]])
        return recursive_get(field_name, mapping)

    except Exception:
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

def populate_object(script, data={}):
    def recursive_populate(script, data):
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
                    recursive_populate(script[key], data)
        else:
            return

    script_copy = dict(**script)
    recursive_populate(script_copy, data)
    return script_copy

def populate_string( yaml_string, data={}):
    """
    max one {{  }} per line!
    """
    def replace_in_line(line):
        if '{{' in line and '}}' in line and not ('#' in line and line.index('#') < line.index('{{')): 
            begin = line.index('{{')
            end = line.index('}}', begin)
            variable_name = line[begin:end].strip().replace('{{','').replace('}}','').strip()
            try:
                value = xeval(variable_name, data)
                return (
                    line[:begin].replace('{{','').replace('}}','') +
                    # value if isinstance(value, (int, float)) else repr(value) +
                    repr(value) +
                    line[end:].replace('}}','').replace('{{','')
                )
            except Exception:
                raise Exception('yaml file needs all data to be evaluated: {{{{ {} }}}}'.format(variable_name))
        else:
            return line
    def replace_multiline(string):
        result = ''
        parts = string.split('{{')
        if len(parts) > 1:
            for part in parts:
                if not '}}' in part:
                    result += part
                else:
                    index = part.index('}}')
                    expr = part[0:index]
                    expr = '\n'.join([line.strip() for line in expr.splitlines()])
                    # print(repr(expr))
                    # print(expr)
                    value = repr(xeval(expr, data))
                    result += value + part[index:].replace('}}', '')
            return result
        else:
            return string
        


    result = '\n'.join(map(replace_in_line, yaml_string.splitlines()))
    result = replace_multiline(result)
    return result


def locate_variable(script):
    begin = script.index('{{')
    end = script.index('}}', begin )
    return script[begin:end].replace('{{', '').strip()

def xeval(expr, data):
    try:
        return eval(expr, dict(
            random=random,
            env=dotdict(**os.environ),
            operator=operator,
            **data,
            data=data,
            **{name: getattr(funcy, name) for name in funcy.__all__}
            # User=User,
            # Story=Story,
            # Media=Media,
            # Hashtag=Hashtag,
            # Geotag=Geotag
        ))

    except Exception as e:
        print(f'error {e} in xeval for "{expr}""')
        raise


if __name__ == '__main__':
    s = """
    ciao: ok
    other: 
        key: {{
                str(
                    'sdfsdf"sdfsdf'
                )
            }}
        another:
            obj:
                ciao: 4
    another: ok ok
    """
    print(populate_string(s))
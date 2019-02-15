from colorama import init, Fore

from string import Formatter

def get_field_value(field_name, mapping):
    try:
        def recursive_get(field_name, mapping):

                if '.' not in field_name:
                    return mapping[field_name], True
                else:
                    *attrs, = field_name.split('.')
                    return recursive_get(".".join(attrs[1:]), mapping[attrs[0]])
        return recursive_get(field_name, mapping)

    except:
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
        if '{{' in line and '}}' in line:
            begin = line.index('{{')
            end = line.index('}}')
            variable_name = line[begin:end].strip().replace('{{','').replace('}}','').strip()
            if variable_name in data:
                return (
                    line[:begin].replace('{{','').replace('}}','') +
                    str(data[variable_name]) +
                    line[end:].replace('}}','').replace('{{','')
                )
            else:
                return line
        else:
            return line

    new_lines = map(replace_in_line, yaml_string.splitlines())
    return '\n'.join(new_lines)

if __name__ == '__main__':
    x = """

name:                            routine
version:                         1



bots:
    -
        username:                {{ username }}
        password:                {{ password }}
        cookie:                  {{ cookie_path }}
        cache:                   {{ cache_path }}


filter:
        user:
            followers:           x > 50 and x < 1000
            following:           x < 500
        media:
            likers:              x < 1000
            hastags:             not in [sex, porn, child]


actions:

    -
        name:                    like competitors followers
        from_type:               user
        nodes:                   {{ competitors }}
        edges:
            # follow random likers
            - shuffle
            - user_feed:
                amount:          1
            - likers:
                amount:          5
            - filter:
                user:
                    # id:        not bot.cache['followed'].find(identifier=x)
                    is_private:  not x
                    is_verified: not x
            - follow:
                max:             20
            - filter:
                user:
                    is_private:  not x
            - user_feed:
                amount:          2
            - like:
                max:             30
    -
        name:                    follow & like hashtags likers
        from_type:               hashtag
        nodes:                   {{ hashtags }}
        edges:
            - hashtag_feed
            - likers
            - follow:
                amount:          20
            - user_feed
            - like:
                amount:          2
    -
        name:                    follow & like location posts likers
        from_type:               geotag
        nodes:                   {{ locations }}
        edges:
            - geotag_feed
            - likers
            - follow:
                amount:          30
            - user_feed
            - like:
                amount:          2

    """
    data = """
    {
        "username": "__morse",
        "password": "ciuccio99",
        "competitors": ["instagram"],
        "hashtags": ["pizza"],
        "geotags": ["milano"],
        "user_to_repost": ["instagram"],
        "captions": ["heeey"]
    }
    """
    import json
    import yaml
    populated = populate_string(x, json.loads(data))
    print(populated)
    # print(yaml.load(populated))

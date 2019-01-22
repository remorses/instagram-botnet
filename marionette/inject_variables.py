from colorama import init, Fore
from datetime import date
import random
import json

def inject(script, data={}):
    if isinstance(script, dict):
        for (key, value) in script.items():
            if isinstance(value, str):
                if '{{' in value and '}}' in value:
                    try:
                        new_value = value.replace('{{','').replace('}}','')
                        new_value = eval(new_value, dict( random=random, data=date, **data,))
                        script[key] = new_value
                    except Exception as e:
                        init(autoreset=True)
                        print(Fore.RED + 'couldn\'t replace {}},\n{}'.format(value, e))
            else:
                inject(script[key], data)
    else:
        return


if __name__ == '__main__':
    data = dict(
        a=dict(
            b=1,
            c='{{ 1 > 3 }}'
        )
    )
    inject(data)
    print(json.dumps(data, indent=4))

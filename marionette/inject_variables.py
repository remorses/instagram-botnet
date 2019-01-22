from colorama import init, Fore
import random

def inject(script, data={}):
    if isinstance(script, dict):
        for (key, value) in script.items():
            if isinstance(value, str):
                if '{{' in value and '}}' in value:
                    try:
                        new_value = value.replace('{{','').replace('}}','')
                        new_value = eval(new_value, dict(**data, random=random))
                        script[key] = new_value
                    except Exception as e:
                        init(autoreset=True)
                        print(Fore.RED + 'couldn\'t replace {}},\n{}'.format(value, e))
            else:
                inject(script[key], data)
    else:
        return script

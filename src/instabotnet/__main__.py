
import json
from colorama import init, Fore
from .execute import execute
# from .debug import unmask



"""
python -m src /etc/template.yml --data-file /etc/data.json
"""

import sys



def load(file):
    with open(file, 'r') as f:
        return f.read()

if __name__ == '__main__':
    template_path = sys.argv[-1]
    template = load(template_path)
    out = execute(template)
    print(Fore.CYAN + json.dumps(out, indent=4))


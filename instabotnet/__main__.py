import sys
import json
from colorama import init, Fore
from .execute import execute
# from .debug import unmask



"""
python -m src /etc/template.yml --data-file /etc/data.json

"""
import click
# from instamob import execute

if __name__ == '__main__':
    @click.command()
    @click.argument('file', type=str)
    @click.option('--data-file', help='data variables to add in the template file')
    def main(ship, template_path, data_path):
        data= json.load(data_path,)
        template = load(template_path)

        out = execute(template, data)
        init()
        print(Fore.YELLOW + out)


def load(file):
    with open(file, 'r') as f:
        return f.read()

import sys
import yaml
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
        template_file = open(template_path, 'r')
        data_file = open(data_path, 'r')
        template = yaml.load(template_file.read())
        data = json.loads(data_file.read())
        data_file.close()
        template_file.close()

        data = execute(template, data)
        # init()
        # print(Fore.YELLOW + unmask(data))
        execute(template, data)

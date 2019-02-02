import sys
import yaml
from colorama import init, Fore
from .execute import execute
from .debug import unmask


if __name__ == '__main__':
    file = open(sys.argv[-1], 'r')
    script = yaml.load(file.read())
    data = execute(script)
    init()
    print(Fore.YELLOW + unmask(data))

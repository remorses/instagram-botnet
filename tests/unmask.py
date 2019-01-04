from pathlib import Path
import json
import sys
import subprocess
from random import random

sys.path += [str(Path(__file__).resolve().parents[1])]



def unmask(obj):
    data = json.dumps(obj)
    temp_file = temporary_file('temp' + str(random())[2:], data)

    with temp_file.open('w') as file:
        file.write(data)

    cmd = 'cat {0!s} | unmask-json --stream --raw'.format(temp_file)

    ps = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    out = ps.communicate()[0]

    temp_file.unlink()

    # out = subprocess.check_output(
    #     [cmd ], shell=True, stderr=subprocess.PIPE)

    return out.decode('ascii')



def temporary_file(name, content):

    temp_path = Path(__file__).parent / '_temp'

    file = Path(str(temp_path.resolve()) + '/' + name )

    file.parent.exists() or file.parent.mkdir()
    file.exists() or file.touch()

    return file.resolve()

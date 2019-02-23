from memory_profiler import profile 
from support import load_yaml
import os

USERNAME = os.environ.get('USERNAME')
PASSWORD = os.environ.get('PASSWORD')



@profile
def main():

    from instabotnet import execute
    
    execute(
        load_yaml('test.yml'), 
        dict(
            username=USERNAME, 
            password=PASSWORD
        )
    )
    
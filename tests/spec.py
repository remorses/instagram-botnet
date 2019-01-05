import sys
from pathlib import Path
import json

from marionette import execute, prepare
from .parse import parse
from .unmask import unmask


################################################################################

SCRIPTS = [
    # parse('tests/hashtags.yml'),
    # parse('tests/geotag_feed.yml'),
    # parse('tests/geotag.yml'),
    # parse('tests/usertags.yml'),
    # parse('tests/like.yml'),
    # parse('tests/authors.yml'),
    # parse('tests/hashtag_feed.yml'),
    # parse('tests/followers.yml'),
    # parse('tests/user_feed.yml'),
    # parse('tests/likers.yml'),
    parse('tests/complex.yml'),
    # parse('tests/upload.yml'),
    # parse('tests/delete.yml'),

]

################################################################################


if __name__ == '__main__':

    data = {}
    for script in SCRIPTS:
        bots = prepare(script)
        data[script['name']] = execute(script, bots)




    for name, raw in data.items():

        ok = False

        with open('tests/artifacts/{}.json'.format(name), 'w+') as file:
            content = file.read()
            json = json.dumps(raw, indent=4)
            if len(raw) > len(json):
                ok = True
                file.write(data)
            else:
                file.write(content)

        with open('tests/artifacts/{}.graphql'.format(name), 'w+') as file:
            content = file.read()

            if ok:
                file.write(unmask(raw))
            else:
                file.write(content)

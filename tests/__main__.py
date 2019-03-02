import sys
from pathlib import Path
import json

from instabotnet import execute

from .parse import parse, load
from .unmask import unmask


################################################################################

SCRIPTS = [
    # load('tests/hashtags.yml'),
    # load('tests/geotag_feed.yml'),
    # load('tests/geotag.yml'),
    # load('tests/usertags.yml'),
    # load('tests/like.yml'),
    # load('tests/authors.yml'),
    # load('tests/hashtag_feed.yml'),
    # load('tests/followers.yml'),
    # load('tests/user_feed.yml'),
    # load('tests/likers.yml'),
    # load('tests/complex.yml'),
    # load('tests/scrape.yml'),
    # load('tests/upload.yml'),
    # load('tests/delete.yml'),
    # load('tests/set_profile.yml'),
    # load('tests/network_bandwidth.yml'),
    # load('tests/stories.yml'),
    # load('tests/text.yml'),
    load('tests/basic.yml'),
    #load('tests/unfollow_non_followers.yml'),

]

################################################################################


if __name__ or '__main__':



        # net_logger = Network_logger()
        # net_logger.daemon = True
        # net_logger.start()

        data = {}
        for script in SCRIPTS:
            execute(script)

        # for name, raw in data.items():
        #
        #     ok = False
        #
        #     with open('tests/artifacts/{}.json'.format(name), 'w+') as file:
        #         content = file.read()
        #         dumped = json.dumps(raw, indent=4)
        #         if len(dumped) > len(content):
        #             ok = True
        #             file.write(dumped)
        #         else:
        #             file.write(content)
        #
        #     with open('tests/artifacts/{}.graphql'.format(name), 'w+') as file:
        #         content = file.read()
        #
        #         if ok:
        #             file.write(unmask(raw))
        #         else:
        #             file.write(content)

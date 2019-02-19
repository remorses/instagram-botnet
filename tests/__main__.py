import sys
from pathlib import Path
import json

from instabotnet import execute

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
    # parse('tests/complex.yml'),
    # parse('tests/scrape.yml'),
    # parse('tests/upload.yml'),
    # parse('tests/delete.yml'),
    # parse('tests/set_profile.yml'),
    # parse('tests/network_bandwidth.yml'),
    # parse('tests/stories.yml'),
    # parse('tests/text.yml'),
    parse('tests/comment.yml'),
    #parse('tests/unfollow_non_followers.yml'),

]

################################################################################


if __name__ or '__main__':



        # net_logger = Network_logger()
        # net_logger.daemon = True
        # net_logger.start()

        data = {}
        for script in SCRIPTS:
            data[script['name']] = execute(script)

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

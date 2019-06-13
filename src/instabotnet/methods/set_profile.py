from funcy import ignore
from ..bot import Bot
from .common import decorate
from ..nodes import Arg
import urllib.request

def download_media(url):
        data = urllib.request.urlopen(url).read()
        # print(fleep.get(data[:300]).extension)
        return data


def load(path):
    with open(path, 'rb') as f:
        return f.read()

"""
Root:
    external_url: Str
    phone_number: Str
    username: Str
    first_name: Str
    biography: Str
    email: Str
    gender: Str
    mode: "public" | "private"
    profile_pic: Path | Url

Path: Str
Url: Str
"""

@decorate(accepts=Arg, returns=Arg)
def edit_profile(bot: Bot, nodes,  args):

    @ignore((KeyError, AttributeError), None)
    def pick(key):
        return args.get(key)

    mode = pick('mode')
    profile_pic = pick('profile_picture')
    # first_name, biography, external_url, email, phone_number, gender
    edits = {
        'external_url': pick('external_url'),
        'phone_number': pick('phone_number'),
        'username': pick('username'),
        'first_name': pick('first_name'),
        'biography': pick('biography'),
        'email': pick('email'),
        'gender': pick('gender'),
    }

    if mode:
        if mode == 'public':
            bot.api.set_public_account()
        elif mode == 'private':
            bot.api.set_private_account()
        else:
            bot.logger.error('{} is not either "public" or "private"'.format(mode))

    
    if profile_pic:
        if 'http' in profile_pic:
            bot.api.change_profile_picture(download_media(profile_pic))
        else:
            bot.api.change_profile_picture(load(profile_pic))

    # TODO set default values in edits
    if any([value for value in edits.values()]):
        new_values = {key: value for key, value in edits.items() if value}
        bot.api.edit_profile(**new_values)

    bot.logger.info('changed profile values')

    return nodes, {}

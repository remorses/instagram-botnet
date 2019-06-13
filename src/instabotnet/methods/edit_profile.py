from funcy import ignore
from ..bot import Bot
from .common import decorate
from ..nodes import node_classes, User
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
    privacy: "public" | "private"
    profile_pic: Path | Url

Path: Str
Url: Str
"""

@decorate(accepts=node_classes.values(), returns=User)
def edit_profile(bot: Bot, nodes,  args):

    @ignore((KeyError, AttributeError), None)
    def pick(key, default=None):
        return args.get(key, default)

    mode = pick('privacy')
    profile_pic = pick('profile_picture')
    # first_name, biography, external_url, email, phone_number, gender
    edits = {
        'external_url': pick('external_url'),
        'phone_number': pick('phone_number'),
        # 'username': pick('username'),
        'first_name': pick('first_name'),
        'biography': pick('biography'),
        'email': pick('email'),
        'gender': 2 if 'f' in pick('gender', '').lower() else 1,
    }

    if mode:
        if mode == 'public':
            bot.api.set_account_private()
        elif mode == 'private':
            bot.api.set_account_public()
        else:
            bot.logger.error('{} is not either "public" or "private"'.format(mode))

    
    if profile_pic:
        if 'http' in profile_pic:
            bot.api.change_profile_picture(download_media(profile_pic))
        else:
            bot.api.change_profile_picture(load(profile_pic))

    # TODO set default values in edits
    if any([value for value in edits.values()]):
        old_values = bot.api.current_user()['user']
        new_values = {key: value if value is not None else old_values[key] for key, value in edits.items()}
        bot.api.edit_profile(**new_values)

    
    bot.logger.info('changed profile values')

    me = bot.api.current_user()['user']
    me = User(**me)

    return [me], {}

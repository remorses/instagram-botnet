from instabotnet.nodes import User, Media
from instabotnet.nodes.media import id_from_url
from instabotnet.bot import Bot
from . import credentials
from funcy import rcompose
from instagram_private_api.utils import InstagramID


bot = Bot(credentials.USERNAME, credentials.PASSWORD)

# data = bot.api.username_info('instagram')['user']
# print(User(**data).id)

url = 'https://www.instagram.com/p/BuPWPLGgl15/'
# data = bot.api.media_info(id_from_url(url))['items'][0]
# print(Media(**data)._json())


print(Media(**rcompose(
    lambda url: [x for x in url.split('/') if x][-1],
    lambda short: InstagramID.expand_code(short),
    lambda id: bot.api.media_info(id),
)(url)['items'][0])._json())

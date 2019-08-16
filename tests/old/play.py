

from instabotnet.bot import Bot
import json

bot = Bot(
    '64578413_',
    'ciuccio99',
    '_settings.json'
)

print(json.dumps(bot.api.user_info('14347589934'), indent=4))
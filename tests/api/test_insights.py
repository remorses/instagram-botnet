

from .support import Bot, env, log, Media

media_url = 'https://www.instagram.com/p/BzlK1m_okaZ/'

def test_statistics():
    bot = Bot(env.username, env.password, env.settings_path, log_level='DEBUG' )
    bot.api.do_login()
    res = bot.api.statistics()
    log(res)


def test_media_insights():
    bot = Bot(env.username, env.password, env.settings_path, log_level='DEBUG' )
    bot.api.do_login()
    pk = Media.id_from_url(media_url)
    res = bot.api.media_insights(pk)
    log(res)
from funcy import wraps, autocurry
from datetime import datetime
import time
from typing import List
from ..nodes import Node
import re


def accepts(Class):

    def _accepts(original):

        @wraps(original)
        def enhanced(bot, nodes,  args):

            # print('nodes in accepts for {}: {}'.format(original.__name__, nodes))

            result = original(bot, nodes,  args)

            return result

        enhanced.accepts = Class

        return enhanced

    return _accepts





def today():
    return datetime.now().strftime("%Y-%m-%d")

def parse_date(date):
    return datetime.strptime(date, "%Y-%m-%d" )





def cycled_api_call(amount, bot, api_method, api_argument, key):

    amount = amount or 9999

    next_max_id = ''
    sleep_track = 0
    done = 0


    while True:
        bot.logger.debug('new get cycle with %s' % api_method.__name__)
        try:
            api_method(api_argument, max_id=next_max_id)
            items = bot.last[key] if key in bot.last else []
            size = len(items)

            if any([
                'next_max_id' not in bot.last,
                "more_available" in bot.last and not bot.last["more_available"],
                "big_list" in bot.last and not bot.last['big_list']
            ]):
                yield from items[:amount - done]
                done += size
                return

            # elif (done + size) >= max:
            #     yield from items[:(max - done)]
            #     done += size
            #     return

            else:
                yield from items[:amount - done]
                done += size
                if done > amount:
                    return

        except Exception as exc:
            bot.logger.error('exception in cycled_api_call: {}'.format(exc))
            yield from []
            return

        if sleep_track > 10:
            bot.logger.debug('sleeping some time while getting')
            bot.sleep('getter')
            sleep_track = 0

        bot.sleep('usual')
        next_max_id = bot.last.get("next_max_id", "")
        sleep_track += 1


def tap(x, lazy_fun):
    lazy_fun()
    return x


def propagate(exc):
    raise exc



class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


def extract_urls(text):
    url_regex = r'((?:(?:http|https|Http|Https|rtsp|Rtsp)://(?:(?:[a-zA-Z0-9$\-\_\.\+\!\*\'\(\)\,\;\?\&\=]|(?:%[a-fA-F0-9]{2})){1,64}(?::(?:[a-zA-Z0-9$\-\_\.\+\!\*\'\(\)\,\;\?\&\=]|(?:%[a-fA-F0-9]{2})){1,25})?@)?)?(?:(?:(?:[a-zA-Z0-9\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF\_][a-zA-Z0-9\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF\_\-]{0,64}\.)+(?:(?:aero|arpa|asia|a[cdefgilmnoqrstuwxz])|(?:biz|b[abdefghijmnorstvwyz])|(?:cat|com|coop|c[acdfghiklmnoruvxyz])|d[ejkmoz]|(?:edu|e[cegrstu])|f[ijkmor]|(?:gov|g[abdefghilmnpqrstuwy])|h[kmnrtu]|(?:info|int|i[delmnoqrst])|(?:jobs|j[emop])|k[eghimnprwyz]|l[abcikrstuvy]|(?:mil|mobi|museum|m[acdeghklmnopqrstuvwxyz])|(?:name|net|n[acefgilopruz])|(?:org|om)|(?:pro|p[aefghklmnrstwy])|qa|r[eosuw]|s[abcdeghijklmnortuvyz]|(?:tel|travel|t[cdfghjklmnoprtvwz])|u[agksyz]|v[aceginu]|w[fs]|(?:\u03B4\u03BF\u03BA\u03B9\u03BC\u03AE|\u0438\u0441\u043F\u044B\u0442\u0430\u043D\u0438\u0435|\u0440\u0444|\u0441\u0440\u0431|\u05D8\u05E2\u05E1\u05D8|\u0622\u0632\u0645\u0627\u06CC\u0634\u06CC|\u0625\u062E\u062A\u0628\u0627\u0631|\u0627\u0644\u0627\u0631\u062F\u0646|\u0627\u0644\u062C\u0632\u0627\u0626\u0631|\u0627\u0644\u0633\u0639\u0648\u062F\u064A\u0629|\u0627\u0644\u0645\u063A\u0631\u0628|\u0627\u0645\u0627\u0631\u0627\u062A|\u0628\u06BE\u0627\u0631\u062A|\u062A\u0648\u0646\u0633|\u0633\u0648\u0631\u064A\u0629|\u0641\u0644\u0633\u0637\u064A\u0646|\u0642\u0637\u0631|\u0645\u0635\u0631|\u092A\u0930\u0940\u0915\u094D\u0937\u093E|\u092D\u093E\u0930\u0924|\u09AD\u09BE\u09B0\u09A4|\u0A2D\u0A3E\u0A30\u0A24|\u0AAD\u0ABE\u0AB0\u0AA4|\u0B87\u0BA8\u0BCD\u0BA4\u0BBF\u0BAF\u0BBE|\u0B87\u0BB2\u0B99\u0BCD\u0B95\u0BC8|\u0B9A\u0BBF\u0B99\u0BCD\u0B95\u0BAA\u0BCD\u0BAA\u0BC2\u0BB0\u0BCD|\u0BAA\u0BB0\u0BBF\u0B9F\u0BCD\u0B9A\u0BC8|\u0C2D\u0C3E\u0C30\u0C24\u0C4D|\u0DBD\u0D82\u0D9A\u0DCF|\u0E44\u0E17\u0E22|\u30C6\u30B9\u30C8|\u4E2D\u56FD|\u4E2D\u570B|\u53F0\u6E7E|\u53F0\u7063|\u65B0\u52A0\u5761|\u6D4B\u8BD5|\u6E2C\u8A66|\u9999\u6E2F|\uD14C\uC2A4\uD2B8|\uD55C\uAD6D|xn--0zwm56d|xn--11b5bs3a9aj6g|xn--3e0b707e|xn--45brj9c|xn--80akhbyknj4f|xn--90a3ac|xn--9t4b11yi5a|xn--clchc0ea0b2g2a9gcd|xn--deba0ad|xn--fiqs8s|xn--fiqz9s|xn--fpcrj9c3d|xn--fzc2c9e2c|xn--g6w251d|xn--gecrj9c|xn--h2brj9c|xn--hgbk6aj7f53bba|xn--hlcj6aya9esc7a|xn--j6w193g|xn--jxalpdlp|xn--kgbechtv|xn--kprw13d|xn--kpry57d|xn--lgbbat1ad8j|xn--mgbaam7a8h|xn--mgbayh7gpa|xn--mgbbh1a71e|xn--mgbc0a9azcg|xn--mgberp4a5d4ar|xn--o3cw4h|xn--ogbpf8fl|xn--p1ai|xn--pgbs0dh|xn--s9brj9c|xn--wgbh1c|xn--wgbl6a|xn--xkc2al3hye2a|xn--xkc2dl3a5ee0h|xn--yfro4i67o|xn--ygbi2ammx|xn--zckzah|xxx)|y[et]|z[amw]))|(?:(?:25[0-5]|2[0-4][0-9]|[0-1][0-9]{2}|[1-9][0-9]|[1-9])\.(?:25[0-5]|2[0-4][0-9]|[0-1][0-9]{2}|[1-9][0-9]|[1-9]|0)\.(?:25[0-5]|2[0-4][0-9]|[0-1][0-9]{2}|[1-9][0-9]|[1-9]|0)\.(?:25[0-5]|2[0-4][0-9]|[0-1][0-9]{2}|[1-9][0-9]|[0-9])))(?::\d{1,5})?(?:/(?:(?:[a-zA-Z0-9\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF\;\/\?\:\@\&\=\#\~\-\.\+\!\*\'\(\)\,\_])|(?:%[a-fA-F0-9]{2}))*)?)(?:\b|$)'
    urls = re.findall(url_regex, text)

    return urls


effify = lambda non_f_str: f'{non_f_str}'
substitute_vars = lambda txt, **kwds: effify(txt).format(**kwds)

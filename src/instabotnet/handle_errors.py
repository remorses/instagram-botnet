
from .api.instagram_private_api.errors import (
    ClientError,
    ClientLoginRequiredError,
    ClientCookieExpiredError,
    ClientConnectionError,
    ClientThrottledError,
    ClientReqHeadersTooLargeError,
)

from .bot import Bot

def handle(func, bot: Bot):
        try:
            return func()
            
        except ClientLoginRequiredError as e:
            bot.logger.error(str(e))
            bot.relogin()
            return func()

        except ClientConnectionError as e:
            bot.logger.error(str(e))

        except (ClientReqHeadersTooLargeError, ClientThrottledError) as e:
            bot.logger.error(str(e))
            bot.sleep(5 * 60)
            return func()

        except ClientError as e:
            if 'consent_required' in str(e).lower():
                bot.logger.error('catched ' + str(e))
                bot.api.agree_consent1()
                bot.api.agree_consent2()
                bot.api.agree_consent3()
                bot.api.do_login()
                return func()
            elif 'not authorized' in str(e).lower():
                return func()
            else:
                raise e from None

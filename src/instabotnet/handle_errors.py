
from instagram_private_api.errors import (
    ClientError,
    ClientLoginRequiredError,
    ClientCookieExpiredError,
    ClientConnectionError,
    ClientThrottledError,
    ClientReqHeadersTooLargeError,
)

def handle(func, bot):
        try:
            return func()
        except ClientLoginRequiredError as e:
            bot.logger.error(str(e))
            bot.relogin()

        except ClientConnectionError as e:
            bot.logger.error(str(e))

        except (ClientReqHeadersTooLargeError, ClientThrottledError) as e:
            bot.logger.error(str(e))
            bot.sleep(5 * 60)

        except ClientError as e: # when trying to see private user
            bot.logger.error(str(e))
            bot.sleep()

        except ClientError as e:
            if 'consent_required' in str(e):
                print('catched', str(e))
                bot.api.agree_consent1()
                bot.api.agree_consent2()
                bot.api.agree_consent3()
                bot.api.do_login()
            else:
                raise e from None
        except Exception as e:
            bot.logger.error('unexpected exception {e}')
            raise e from None

from instabot import API as NOT_MY_API
from instabot.api import config, devices
from colorlog import ColoredFormatter
import logging
from .html_log import HTMLFileHandler, HTMLFormatter
import json
from json.decoder import JSONDecodeError

import time
class LoggerAdapter(logging.LoggerAdapter):
    def __init__(self, logger, prefix):
        super(LoggerAdapter, self).__init__(logger, {})
        self.prefix = prefix

    def process(self, msg, kwargs):
        return '[%s] %s' % (self.prefix, msg), kwargs

class API(NOT_MY_API):

    id = 0

    def __init__(self, logs_file, device=None, username=None,  id=None):

        self.id = API.id if not id else id
        API.id += 1
        # Setup device and user_agent
        device = device or devices.DEFAULT_DEVICE
        self.device_settings = devices.DEVICES[device]
        self.user_agent = config.USER_AGENT_BASE.format(**self.device_settings)

        self.is_logged_in = False
        self.last_response = None
        self.total_requests = 0

        # Setup logging





        self.logger = logging.getLogger('[{}]'.format(self.id))

        # fh = HTMLFileHandler(title=self.id, file=logs_file, mode='w')
        # fh.setLevel(logging.INFO)
        # fh.setFormatter(file_formatter())
        # self.logger.addHandler(fh)

        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(colred_formatter())
        self.logger.addHandler(ch)

        self.logger.setLevel(logging.DEBUG)
        self.logger = LoggerAdapter(self.logger, username)



        self.last_json = None

    def media_info(self, media_id):
        url = 'media/{media_id}/info/'.format(media_id=media_id)
        return self.send_request(url)


    def send_request(self, endpoint, post=None, login=False, with_signature=True):
            self.logger.info('new request to endpoint %s' % endpoint)
            if (not self.is_logged_in and not login):
                msg = "Not logged in!"
                self.logger.critical(msg)
                raise Exception(msg)

            self.session.headers.update(config.REQUEST_HEADERS)
            self.session.headers.update({'User-Agent': self.user_agent})
            try:
                self.total_requests += 1
                if post is not None:  # POST
                    if with_signature:
                        # Only `send_direct_item` doesn't need a signature
                        post = self.generate_signature(post)
                    response = self.session.post(
                        config.API_URL + endpoint, data=post)
                else:  # GET
                    response = self.session.get(
                        config.API_URL + endpoint)
            except Exception as e:
                self.logger.warning(str(e))
                return False

            if response.status_code == 200:
                self.last_response = response
                try:
                    self.last_json = json.loads(response.text)
                    return True
                except JSONDecodeError:
                    return False
            else:
                self.logger.error("Request returns {} error!".format(response.status_code))
                if response.status_code == 429:
                    sleep_minutes = 5
                    self.logger.warning(
                        "That means 'too many requests'. I'll go to sleep "
                        "for {} minutes.".format(sleep_minutes))
                    time.sleep(sleep_minutes * 60)
                elif response.status_code == 400:
                    response_data = json.loads(response.text)
                    msg = "Instagram's error message: {}"
                    self.logger.info(msg.format(response_data.get('message')))
                    if 'error_type' in response_data:
                        msg = 'Error type: {}'.format(response_data['error_type'])
                        self.logger.info(msg)

                # For debugging
                try:
                    self.last_response = response
                    self.last_json = json.loads(response.text)
                except Exception:
                    pass
                return False

    def edit_profile(self, external_url, phone_number, full_name, biography, email, gender, **rest):
        data = self.json_data({
            'external_url': external_url,
            'phone_number': phone_number,
            'username': self.username,
            'full_name': full_name,
            'biography': biography,
            'email': email,
            'gender': gender,
        })
        return self.send_request('accounts/edit_profile/', data)

    def get_story_feed(self, user_id):
        """
        last_json will have the form:
        {
            reel:
                items: {
                ...
                }
                id
                user
                expiring_at
                location
                reel_type
                title
                ...
            }
        }
        """
        url = "feed/user/{user_id}/story/".format(user_id=user_id)
        return self.send_request(url)


def colred_formatter():
    format = '%(asctime)s | %(levelname)-8s | %(message)s'
    cformat = '%(log_color)s' + format
    date_format = '%Y-%m-%d %H:%M'
    return ColoredFormatter(cformat, date_format,
                            log_colors={'DEBUG': 'reset', 'INFO': 'green',
                                        'WARNING': 'yellow', 'ERROR': 'red',
                                        'CRITICAL': 'red'})


def file_formatter():
    format = '%(asctime)s | %(levelname)-8s | %(message)s'
    cformat = '%(log_color)s' + format
    date_format = '%Y-%m-%d %H:%M'
    return HTMLFormatter(cformat, date_format,)



def tap(x, function):
    function()
    return x

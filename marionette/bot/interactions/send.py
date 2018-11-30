from ..nodes import User, Media
from ..bot import Bot


def send(self: Bot, args):
    for user in self._acc:
        if isinstance(user, User):
            id = user.id
        else:
            id = User.get_user_id(user)

        for message in args['messages']:
            for type, arg in message.items()[0]:
                if type == 'text':
                    _send_text(self, arg, id)
                elif type == 'media':
                    pass
                elif type == 'profile':
                    pass
                elif type == 'hashtag':
                    pass


def _send_text(self: Bot, text, user_id, thread_id=None):
    """
    :param self: bot
    :param text: text of message
    :param user_ids: list of user_ids for creating group or one user_id for send to one person
    :param thread_id: thread_id
    """

    if not isinstance(text, str) and isinstance(user_id, (str)):
        self.logger.info.error(
            'Text must be an string, user_ids must be an list or string')
        return False

    if self.reached_limit('messages'):
        self.logger.info.info("Out of messages for today.")
        return False

    self.delay('message')
    urls = self.extract_urls(text)
    item_type = 'link' if urls else 'text'
    if self._api.send_direct_item(
            item_type,
            user_id,
            text=text,
            thread=thread_id,
            urls=urls
            ):
        self.total['messages'] += 1
        return True

    self.logger.info.info(
        "Message to {user_id} wasn't sent".format(user_id))
    return False

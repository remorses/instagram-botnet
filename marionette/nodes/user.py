from .node import Node
from .common import attributes


def username_from_id(id):
    pass


class User(Node):

    def __init__(self, *, generic=None, id=None, username=None, is_private=None, data=None):
        self._username = username
        self._id = id
        self._data = data
        self._is_private = is_private


        if generic:
            self._username = generic

    def __repr__(self):
        username, id, data, *rest = attributes(self)

        if username:
            return 'User(username=\'{}\')'.format(username)
        elif id:
            return 'User(id=\'{}\')'.format(id)
        elif data:
            return 'User(data=\'{...}\')'

    @property
    def username(self):
        username, id, data,  *rest = attributes(self)

        if username:
            return username
        elif id:
            return username_from_id(id)
        elif data:
            return data['user']['username']
        else:
            return False

    @property
    def id(self):
        username, id, data, *rest = attributes(self)
        if id:
            return id
        elif data:
            return data['user']['username']
        else:
            return False

    @property
    def is_private(self):
        _, _, _, is_private = attributes(self)

        if is_private:
            return is_private
        else:
            return False

    def get_id(self, bot):
        if self.username:
            bot.api.search_username(self.username)
            if "user" in bot.api.last_json:
                return str(bot.api.last_json["user"]["pk"])
        else:
            raise Exception('username is needed to get the id')


    def get_followers_count(self, bot):
        if self.username:
            bot.api.get_username_info(self.id)
            if "user" in bot.api.last_json:
                return str(bot.api.last_json["user"]["follower_count"])
        else:
            raise Exception('id is needed to get the count')


    def get_following_count(self, bot):
        if self.username:
            bot.api.get_username_info(self.id)
            if "user" in bot.api.last_json:
                return str(bot.api.last_json["user"]["following_count"])
        else:
            raise Exception('id is needed to get the count')

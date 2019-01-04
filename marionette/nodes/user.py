from .node import Node
from .common import attributes



class User(Node):

    def __init__(self, *, generic=None, id=None, username=None, is_private=None, data=None):
        self._username = username
        self._id = id
        self._data = data

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
        username, id, data = attributes(self)
        if username:
            return username
        elif data:
            return data['username']
        else:
            return False

    @property
    def id(self):
        username, id, data, *rest = attributes(self)
        if id:
            return id
        elif data:
            return data['pk']
        else:
			return False


    def get_data(self, bot):
	    username, id, data = attributes(self)
        if id:
            bot.api.get_username_info(id)
            if 'user' in bot.last:
                self._data = bot.last['user']
                return self._data
		elif data:
			if 'pk' in data:
				self._id = data['pk']
				return self.get_data(bot)
			else:
				return False
        elif username:
            bot.api.search_username(username)
            if 'user' in bot.last:
	            self._data = bot.last['user']
	            self._data = self.get_data(bot)
                return self._data
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
	    username, id, data = attributes(self)
	    if id:
		    return id
	    elif data:
		    if 'pk' in data:
			    return data['pk']
        elif username:
            data = self.get_data(bot)
            return data['pk']
		else:
            return False


    def get_followers_count(self, bot):
	    _, _, data = attributes(self)
        if 'follower_count' in data:
            return data['follower_count']
        else:
	        data = self.get_data(bot)
	        return data['follower_count']


    def get_following_count(self, bot):
	    _, _, data = attributes(self)
        if 'following_count' in data:
            return data['following_count']
        else:
	        data = self.get_data(bot)
	        return data['following_count']


    def get_is_private(self, bot):
	    _, _, data = attributes(self)
        if 'is_private' in data:
            return data['is_private']
        else:
	        data = self.get_data(bot)
	        return data['is_private']


    def get_is_business(self, bot):
	    _, _, data = attributes(self)
        if 'is_business' in data:
            return data['is_business']
        else:
	        data = self.get_data(bot)
	        return data['is_business']

    def get_is_verified(self, bot):
	    _, _, data = attributes(self)
        if 'is_verified' in data:
            return data['is_verified']
        else:
	        data = self.get_data(bot)
	        return data['is_verified']

    def get_is_anonymous_picture(self, bot):
	    _, _, data = attributes(self)
        if 'has_anonymous_profile_picture' in data:
            return data['has_anonymous_profile_picture']
        else:
	        data = self.get_data(bot)
	        return data['has_anonymous_profile_picture']

    def get_bio(self, bot):
	    _, _, data = attributes(self)
        if 'biography' in data:
            return data['biography']
        else:
	        data = self.get_data(bot)
	        return data['biography']

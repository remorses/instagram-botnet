from typing import List
from .nodes import User, Media, Hashtag, Geotag, Usertag
from .extent import Extent


class Interactions(Extent):

    def like(self, args):

        print('medias: ', self._acc)

        for media in self._acc:
            if isinstance(media, Media):
                id = media.id
            else:
                url = media
                id = Media.get_media_id_from_link(url)
                print('id: {}'.format(id))

            if self._api.like(id):
                print('liked media %d.' % id)
            else:
                print('can\'t like')

        self._reset()

    # def media_author(self, medias: List[Media]) -> List[User]:
    #     result = []
    #     for media in medias:
    #         if self.api.media_info(media.id):
    #             author_id = str(self.api.last_json["items"][0]["user"]["pk"])
    #             result += [User(id=author_id)]
    #     self._accumulate([])

    def comment(self, users: List[Media]):
        pass

    def report(self, users: List[Media]):
        pass

    def follow(self, medias: List[User]):
        pass

    def block(self, medias: List[User]):
        pass

    def send(self, args):
        for user in self._acc:
            if isinstance(user, User):
                id = user.id
            else:
                id = User.get_user_id(user)

            for message in args['messages']:
                for type, arg in message.items()[0]:
                    if type == 'text':
                        self._send_message(arg, id)
                    elif type == 'media':
                        pass
                    elif type == 'profile':
                        pass
                    elif type == 'hashtag':
                        pass

    def _send_message(self, text, user_id, thread_id=None):
        """
        :param self: bot
        :param text: text of message
        :param user_ids: list of user_ids for creating group or one user_id for send to one person
        :param thread_id: thread_id
        """

        if not isinstance(text, str) and isinstance(user_id, (str)):
            self.logger.error(
                'Text must be an string, user_ids must be an list or string')
            return False

        if self.reached_limit('messages'):
            self.logger.info("Out of messages for today.")
            return False

        self.delay('message')
        urls = self.extract_urls(text)
        item_type = 'link' if urls else 'text'
        if self.api.send_direct_item(
                item_type,
                user_id,
                text=text,
                thread=thread_id,
                urls=urls
                ):
            self.total['messages'] += 1
            return True

        self.logger.info(
            "Message to {user_id} wasn't sent".format(user_id))
        return False


# methods = {
#     'like': like,
#     'comment': comment,
#     'report': report,
#
#     'follow': follow,
#     'send': send,
#     'block': block
# }

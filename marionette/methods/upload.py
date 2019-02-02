from typing import List
import requests
from random import random
from pathlib import Path
from funcy import take
from itertools import islice
from .common import accepts, today
from ..nodes import Node, Arg, Media
import time




@accepts(Arg)
def upload(bot, nodes,  args):

    max = args.get('max') or 1
    nodes = islice(nodes, max)
    nodes = list(nodes)
    if len(nodes) == 0:
        bot.logger.error('no photos to upload')




    if max == 1:
        type = 'photo'

        node = take(1, nodes)[0]

        if isinstance(node, Arg):
            value = node.value
        elif isinstance(node, Media):
            value = node.url
        else:
            value = node

        caption = args['caption'] if 'caption' in args else None
        # TODO implement geotag and usertag in uploading
        # geotag = args[geotag] if 'geotag' in args else None
        # usertags = args[usertags] if 'usertags' in args else None



        if 'instagram.com' in value:
            media_id = Media(url=value).id
            bot.api.media_info(media_id)
            media = bot.last['items'][0]
            type = media_type(media)
            if type == 'photo':
                temp = TempImage(Path(bot.cache_file).parent)
                path = bot.api.download_photo(media_id, temp.path, media=media)
            else:
                temp = TempVideo(Path(bot.cache_file).parent)
                path = bot.api.download_video(media_id, temp.path, media=media)

        elif value.startswith(('http', 'https')):
            url = value
            if url.endswith(('.jpg', '.jpeg')):
                type = 'photo'
                temp = TempImage(Path(bot.cache_file).parent)
            elif url.endswith(('.mp4', '.mov')):
                type = 'video'
                temp = TempVideo(Path(bot.cache_file).parent)
            else:
                raise Exception('to use http url it must end with .jpg or .mp4 or .mov to notify file type')
            path = download_media(bot, url, temp.path)

        else:
            path = str(Path(value).resolve())
            if path.endswith(('.jpg', '.jpeg')):
                type = 'photo'
            elif path.endswith(('.mp4', '.mov')):
                type = 'video'
            else:
                raise Exception('media must be .jpg or .mp4 or .mov')




        if type == 'photo':
            if not bot.api.upload_photo(path, caption):
                bot.logger.warn('upload failed')
            else:
                bot.total['uploads'] += 1
        else:
            if not bot.api.upload_video(path, caption):
                bot.logger.warn('upload failed')

        temp.delete()

        # with bot.cache as cache:
        #     cache['uploaded'].insert(dict(identifier=bot.last, url=media.url, time=today(), type='media'))

        bot.logger.debug('sleeping some time')
        bot.sleep('upload')

    else:
        # upload album
        pass

    return [], bot.last


class TempImage():
    def __init__(self, folder):
        self.filename = str(random())[2:] + '.jpg'
        self._path = Path(folder).resolve() / self.filename
        self._path.exists() or self._path.touch()

    def delete(self):
        self._path.unlink()

    @property
    def path(self):
        return str(self._path)


class TempVideo():
    def __init__(self, folder):
        self.filename = str(random())[2:] + '.mov'
        self._path = Path(folder).resolve() / self.filename
        self._path.exists() or self._path.touch()


    def delete(self):
        self._path.unlink()

    @property
    def path(self):
        return str(self._path)



def download_media(bot, url, file_path):
        response = bot.session.get(url, stream=True)
        if response.status_code == 200:
                with open(file_path, 'wb') as f:
                    for chunk in response:
                        f.write(chunk)
        return str(Path(file_path).resolve())


def media_type(media):
    if media['media_type'] == 1:
        return 'photo'
    elif media['media_type'] == 2:
        return 'video'
    else:
        first_media = media["carousel_media"][0]["media_type"]
        return media_type(first_media)

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
            resize_image(path)

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






def resize_image(fname):
    from math import ceil
    try:
        from PIL import Image, ExifTags
    except ImportError as e:
        print("ERROR: {}".format(e))
        print("Required module `PIL` not installed\n"
              "Install with `pip install Pillow` and retry")
        return False
    print("Analizing `{}`".format(fname))
    h_lim = {'w': 90., 'h': 47.}
    v_lim = {'w': 4., 'h': 5.}
    img = Image.open(fname)
    (w, h) = img.size
    deg = 0
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        exif = dict(img._getexif().items())
        o = exif[orientation]
        if o == 3:
            deg = 180
        if o == 6:
            deg = 270
        if o == 8:
            deg = 90
        if deg != 0:
            print("Rotating by {d} degrees".format(d=deg))
            img = img.rotate(deg, expand=True)
            (w, h) = img.size
    except (AttributeError, KeyError, IndexError) as e:
        print("No exif info found (ERR: {})".format(e))
        pass
    img = img.convert("RGBA")
    ratio = w * 1. / h * 1.
    print("FOUND w:{w}, h:{h}, ratio={r}".format(w=w, h=h, r=ratio))
    if w > h:
        print("Horizontal image")
        if ratio > (h_lim['w'] / h_lim['h']):
            print("Cropping image")
            cut = int(ceil((w - h * h_lim['w'] / h_lim['h']) / 2))
            left = cut
            right = w - cut
            top = 0
            bottom = h
            img = img.crop((left, top, right, bottom))
            (w, h) = img.size
        if w > 1080:
            print("Resizing image")
            nw = 1080
            nh = int(ceil(1080. * h / w))
            img = img.resize((nw, nh), Image.ANTIALIAS)
    elif w < h:
        print("Vertical image")
        if ratio < (v_lim['w'] / v_lim['h']):
            print("Cropping image")
            cut = int(ceil((h - w * v_lim['h'] / v_lim['w']) / 2))
            left = 0
            right = w
            top = cut
            bottom = h - cut
            img = img.crop((left, top, right, bottom))
            (w, h) = img.size
        if h > 1080:
            print("Resizing image")
            nw = int(ceil(1080. * w / h))
            nh = 1080
            img = img.resize((nw, nh), Image.ANTIALIAS)
    else:
        print("Square image")
        if w > 1080:
            print("Resizing image")
            img = img.resize((1080, 1080), Image.ANTIALIAS)
    (w, h) = img.size
    new_fname = "{}.CONVERTED.jpg".format(fname)
    print("Saving new image w:{w} h:{h} to `{f}`".format(w=w, h=h, f=new_fname))
    new = Image.new("RGB", img.size, (255, 255, 255))
    new.paste(img, (0, 0, w, h), img)
    new.save(new_fname, quality=95)
    return new_fname

import imagesize
from funcy import take
import fleep
import json
import urllib.request
import ffmpeg
from .common import decorate, temporary_write
from ..bot import Bot
from ..nodes import Arg, Media
import traceback
from datetime import datetime


SUPPORTED_IMAGE_EXT = ['jpg']
SUPPORTED_VIDEO_EXT = ['mov', 'mp4']


@decorate(accepts=(Arg, Media), returns=Media)
def upload_post(bot: Bot, nodes,  args):
    max = args.get('max') or 1
    caption = args.get('caption') or ''
    geotag = args.get('geotag')
    disable_comments = bool(args.get('disable_comments'))

    nodes = take(max, nodes)
    
    def download_media(url):
        data = urllib.request.urlopen(url).read()
        # print(fleep.get(data[:300]).extension)
        return data

    def binary_data(node):
        is_url = isinstance(node, Arg) and 'http' in node.value
        is_media = isinstance(node, Media)
        is_path = isinstance(node, Arg) and not 'http' in node.value
        switch = {
            is_url: lambda: download_media(node.value),
            is_path: lambda: load(node.value),
            is_media: lambda: download_media(node.images[0]),
        }
        return switch[True]()


    def get_geotag_data(name):
        return bot.api.location_search(bot.latitude, bot.longitude, query=name,)['venues'][0]



    if len(nodes) == 0:
        bot.logger.error('no medias to upload')

    if max == 1: # only 1 media


        node = nodes[0]
        # print(node.carousel_media)
        # print(node.sources[0])
        kwargs = dict(
              caption=caption,
              to_reel=False,
        )

        if geotag:
              kwargs.update(dict(location=get_geotag_data(geotag),))

        if disable_comments is not None:
              kwargs.update(dict(disable_comments=disable_comments))

        data = binary_data(node)
        with temporary_write(data) as path:
                extensions = fleep.get(data[:128]).extension
                ext = extensions[0] if len(extensions) > 0 else None
                if ext in SUPPORTED_IMAGE_EXT:
                    bot.logger.info('uploading img')
                    kwargs.update(make_photo_args(data, path))
                    res = bot.api.post_photo(**kwargs)
                    uploaded_media = Media(**res.get('media',{}))
                    # print(json.dumps(res, indent=4))

                elif ext in SUPPORTED_VIDEO_EXT:
                    bot.logger.info('uploading video')
                    kwargs.update(make_video_args(data, path))
                    res = bot.api.post_video(**kwargs)
                    uploaded_media = Media(**res.get('media',{}))

                else:
                      raise RuntimeError(f'unsupportd media type {fleep.get(data[:128]).extension} for {node}')

                bot.logger.info(f'uploaded media {uploaded_media}')
                
                events = [{
                    'type': 'upload_post',
                    'metadata': bot.metadata,
                    'args': {
                        'caption': caption,
                        'geotag': geotag,
                        'caption': caption,
                        'disable_comments': disable_comments,
                    },
                    'node': {
                        'url': uploaded_media.url,
                        'is_album': False,
                        'type': 'media',
                    },
                    'timestamp': str(datetime.utcnow()),
        }]
                return [uploaded_media], { 'events': events }



    else: # album upload

        uploads= []

        for node in nodes:

            data = binary_data(node)

            with temporary_write(data) as path:
                extensions = fleep.get(data[:128]).extension
                ext = extensions[0] if len(extensions) > 0 else None
                if ext in SUPPORTED_IMAGE_EXT:
                    uploads.append(make_photo_args(data, path))

                elif ext in SUPPORTED_VIDEO_EXT:
                    uploads.append(make_video_args(data, path))

                else:
                    raise RuntimeError(f'unsupportd media type {fleep.get(data[:128]).extension} for {node}')

        kwargs = dict(
            caption=caption,
            medias=uploads,
        )

        if geotag:
              kwargs.update(dict(location=get_geotag_data(geotag),))

        # if disable_comments is not None:
        #       kwargs.update(dict(disable_comments=bool(disable_comments)))

        res = bot.api.post_album(**kwargs)
        uploaded_media = Media(**res.get('media',{}))
        bot.logger.info(f'uploaded album {uploaded_media}')
        events = [{
                    'type': 'upload_post',
                    'metadata': bot.metadata,
                    'args': {
                        'caption': caption,
                        'geotag': geotag,
                        'caption': caption,
                        'disable_comments': disable_comments,
                    },
                    'node': {
                        'url': uploaded_media.url,
                        'is_album': True,
                        'type': 'media',
                    },
                    'timestamp': str(datetime.utcnow()),
        }]
        return [uploaded_media], { 'events': events }



def load(path):
    with open(path, 'rb') as f:
        return f.read()





def get_video_size(path):
        probe = ffmpeg.probe(path)
        video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
        width = int(video_stream['width'])
        height = int(video_stream['height'])
        return width, height

def make_thumbnail(input_data, width=100):
    import subprocess
    import ffmpeg

    args = (
        ffmpeg
            .input('pipe:')
            # ... extra processing here
            .filter('scale', width, -1)
            .output('pipe:', vframes=1)
            .get_args()
    )

    p = subprocess.Popen(['ffmpeg'] + args, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    output_data = p.communicate(input=input_data)[0]
    return output_data

def get_video_duration(path):
        duration = ffmpeg.probe(path)['format']['duration']
        return float(duration)

def make_photo_args(data, path):
    return dict(
        photo_data=data,
        data=data,
        size=imagesize.get(path),
        type='image',
    )

def make_video_args(data, path):
    return dict(
        video_data=data,
        data=data,
        thumbnail_data=make_thumbnail(data),
        duration=get_video_duration(path),
        size=get_video_size(path),
        type='video',
    )

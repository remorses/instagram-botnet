import imagesize
from funcy import take
from .common import decorate, temporary_write
from ..nodes import Arg, Media



SUPPORTD_IMAGE_EXT = ['jpg']
SUPPORTD_VIDEO_EXT = ['mov']


@decorate(accepts=(Arg, Media), returns=Media)
def upload_post(bot, nodes,  args):

    max = args.get('max') or 1
    caption = args.get('caption') or ''
    geotag = args.get('geotag')
    disable_comments = args.get('disable_comments')
    
    
    nodes = take(max, nodes)

    if len(nodes) == 0:
        bot.logger.error('no medias to upload')

    if max == 1: # only 1 media
            
        node = nodes[0]
        
        
        kwargs = dict(
              caption=caption,  
              to_reel=False, 
        )
        
        if geotag:
              kwargs.update(dict(location=get_geotag_data(geotag),))
        
        if disable_comments is not None:
              kwargs.update(dict(disable_comments=bool(disable_comments)))
              
        data = binary_data(node)
        with temporary_write(data) as path:     
                if fleep.get(data[:128]).extension[0] in SUPPORTD_IMAGE_EXT:
                      kwargs.update(get_photo_args(data, path))
                      res = bot.api.post_photo(**kwargs)
                      
                elif fleep.get(data[:128]).extension[0] in SUPPORTD_VIDEO_EXT:
                      kwargs.update(make_video_args(data, path))
                      res = bot.api.post_video(**kwargs)
                      
                else:
                      raise RuntimeError(f'unsupportd media type {fleep.get(data[:128]).extension} for {node}')
                      
        
        
    else: # album upload
    
        uploads= []
        
        for node in nodes:
        
            data = binary_data(node)
            
            with temporary_write(data) as path:
                if fleep.get(data[:128]).extension[0] in SUPPORTED_IMAGE_EXT:
                    uploads.append(make_photo_args(data, path) 
                    
                elif fleep.get(data[:128]).extension[0] in SUPPORTED_VIDEO_EXT:
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


        
def load(path):
    with open(path, 'rb') as f:
        return f.read()
            
def download_media(url):
    return urllib.request.urlopen(url).read()
      
def binary_data(node):
    is_url = isinstance(node, Arg) and 'http' in node.value
    is_media = isinstance(node, Media) and node.url
    is_path = is_arg and not 'http' in node.value
    
    switch = {
        is_url: download_media(node.value),
        is_path: load(node.value),
        is_media: download_media(node.url),
    }
    
    return switch[True]

def get_geotag_data(name):
    pass


def get_video_size(path):
        probe = ffmpeg.probe(path)
        video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
        width = int(video_stream['width'])
        height = int(video_stream['height'])
        return width, height

def make_thumbnail(input_data):
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
    )
    
def make_video_args(data, path):
    
    return dict(
        video_data=data,
        data=data,
        thumbnail_data=make_thumbnail(data),
        duration=get_video_duration(path),
        size=get_video_size(path),
    )






from funcy import rcompose, ignore, fallback
from .node import Node
from modeller import Model
import yaml

schema = yaml.load('''
properties:
    can_see_insights_as_brand: {}
    can_view_more_preview_comments: {}
    can_viewer_reshare: {}
    can_viewer_save: {}
    caption:
        properties:
            bit_flags:
                type: integer
            content_type:
                type: string
            created_at:
                type: integer
            created_at_utc:
                type: integer
            did_report_as_spam:
                type: boolean
            has_translation: {}
            media_id:
                type: integer
            pk:
                type: integer
            share_enabled:
                type: boolean
            status:
                type: string
            text:
                type: string
            type:
                type: integer
            user:
                {user_schema}
            user_id:
                type: integer
        required:
            - user
            - created_at
            - text
            - did_report_as_spam
            - share_enabled
            - user_id
            - content_type
            - bit_flags
            - pk
            - status
            - created_at_utc
            - type
            - media_id
        type: object
    caption_is_edited: {}
    carousel_media:
        properties:
            carousel_parent_id: {}
            id: {}
            image_versions2:
                properties:
                    candidates:
                        properties:
                            height: {}
                            url: {}
                            width: {}
                        required:
                            - url
                            - height
                            - width
                required:
                    - candidates
            is_dash_eligible: {}
            media_type: {}
            number_of_qualities: {}
            original_height: {}
            original_width: {}
            pk: {}
            usertags:
                properties:
                    in:
                        properties:
                            duration_in_video_in_sec:
                                type: 'null'
                            position:
                                items:
                                    type: number
                                type: array
                            start_time_in_video_in_sec:
                                type: 'null'
                            user:
                                {user_tag}
                        required:
                            - duration_in_video_in_sec
                            - position
                            - user
                            - start_time_in_video_in_sec
                        type: object
                required:
                    - in
                type: object
            video_codec: {}
            video_dash_manifest: {}
            video_duration: {}
            video_versions:
                properties:
                    height: {}
                    id: {}
                    type: {}
                    url: {}
                    width: {}
                required:
                    - height
                    - width
                    - url
                    - type
                    - id
        required:
            - video_versions
            - original_height
            - video_codec
            - is_dash_eligible
            - original_width
            - number_of_qualities
            - pk
            - carousel_parent_id
            - media_type
            - id
            - video_duration
            - image_versions2
            - video_dash_manifest
    carousel_media_count: {}
    client_cache_key: {}
    code: {}
    comment_count: {}
    comment_likes_enabled: {}
    comment_threading_enabled: {}
    commenting_disabled_for_viewer:
        type: boolean
    comments_disabled:
        type: boolean
    device_timestamp: {}
    direct_reply_to_author_enabled:
        type: boolean
    facepile_top_likers: {}
    filter_type: {}
    has_audio:
        type: boolean
    has_liked: {}
    has_more_comments: {}
    id: {}
    image_versions2:
        properties:
            candidates:
                properties:
                    height: {}
                    url: {}
                    width: {}
                required:
                    - url
                    - height
                    - width
        required:
            - candidates
    inline_composer_display_condition: {}
    inline_composer_imp_trigger_time: {}
    is_dash_eligible: {}
    lat:
        type: number
    like_count: {}
    likers:
        {user_schema}
    lng:
        type: number
    location:
        {geotag_schema}
    max_num_visible_preview_comments: {}
    media_type: {}
    next_max_id:
        type: integer
    number_of_qualities: {}
    organic_tracking_token: {}
    original_height: {}
    original_width: {}
    photo_of_you: {}
    pk: {}
    preview_comments:
        {comment_schema}
    taken_at: {}
    top_likers:
        items:
            type: string
    user:
        {user_schema}
    usertags:
        properties:
            in:
                properties:
                    duration_in_video_in_sec:
                        type: 'null'
                    position:
                        items:
                            type: number
                        type: array
                    start_time_in_video_in_sec:
                        type: 'null'
                    user:
                        {user_schema}
                required:
                    - duration_in_video_in_sec
                    - position
                    - user
                    - start_time_in_video_in_sec
                type: object
        required:
            - in
        type: object
    video_codec: {}
    video_dash_manifest: {}
    video_duration:
        type: number
    video_versions:
        properties:
            height:
                type: integer
            id:
                type: string
            type:
                type: integer
            url:
                type: string
            width:
                type: integer
        required:
            - height
            - width
            - url
            - type
            - id
        type: object
    view_count:
        type: number
required:
    - can_viewer_save
    - photo_of_you
    - caption
    - filter_type
    - user
    - has_liked
    - organic_tracking_token
    - caption_is_edited
    - code
    - can_viewer_reshare
    - like_count
    - taken_at
    - client_cache_key
    - pk
    - media_type
    - id
    - device_timestamp
''')


get_image_url = lambda data: fallback(
    lambda: data['image_versions2']['candidates'][0]['url'],
    lambda: data['image_versions2'][0]['url'],
    lambda: None,
)

get_video_url = lambda data: fallback(
    lambda: data['video_versions'][0]['url'],
    lambda: None,
)

get_url = lambda data: get_video_url(data) or get_image_url(data)

class Media(Node, Model):

    id = property(lambda self: self.pk)

    url = property(lambda self: url_from_id(self.pk))

    sources = property(lambda self: fallback(
        lambda: list(map(get_url, self['carousel_media'])),
        lambda: [get_url(self)],
        lambda: [],
    ))

























def id_from_url(link):
    if 'instagram.com/p/' not in link:
        # self.logger.error('Unexpected link')
        return False
    link = link.split('/')
    code = link[link.index('p') + 1]

    alphabet = {
        '-': 62, '1': 53, '0': 52, '3': 55, '2': 54, '5': 57, '4': 56,
        '7': 59, '6': 58, '9': 61, '8': 60, 'A': 0, 'C': 2, 'B': 1,
        'E': 4, 'D': 3, 'G': 6, 'F': 5, 'I': 8, 'H': 7, 'K': 10, 'J': 9,
        'M': 12, 'L': 11, 'O': 14, 'N': 13, 'Q': 16, 'P': 15, 'S': 18,
        'R': 17, 'U': 20, 'T': 19, 'W': 22, 'V': 21, 'Y': 24, 'X': 23,
        'Z': 25, '_': 63, 'a': 26, 'c': 28, 'b': 27, 'e': 30, 'd': 29,
        'g': 32, 'f': 31, 'i': 34, 'h': 33, 'k': 36, 'j': 35, 'm': 38,
        'l': 37, 'o': 40, 'n': 39, 'q': 42, 'p': 41, 's': 44, 'r': 43,
        'u': 46, 't': 45, 'w': 48, 'v': 47, 'y': 50, 'x': 49, 'z': 51,
        }

    result = 0
    for char in code:
        result = result * 64 + alphabet[char]
    return result


def url_from_id(id):
    id = int(id)
    alphabet = {
        '-': 62, '1': 53, '0': 52, '3': 55, '2': 54, '5': 57, '4': 56,
        '7': 59, '6': 58, '9': 61, '8': 60, 'A': 0, 'C': 2, 'B': 1,
        'E': 4, 'D': 3, 'G': 6, 'F': 5, 'I': 8, 'H': 7, 'K': 10, 'J': 9,
        'M': 12, 'L': 11, 'O': 14, 'N': 13, 'Q': 16, 'P': 15, 'S': 18,
        'R': 17, 'U': 20, 'T': 19, 'W': 22, 'V': 21, 'Y': 24, 'X': 23,
        'Z': 25, '_': 63, 'a': 26, 'c': 28, 'b': 27, 'e': 30, 'd': 29,
        'g': 32, 'f': 31, 'i': 34, 'h': 33, 'k': 36, 'j': 35, 'm': 38,
        'l': 37, 'o': 40, 'n': 39, 'q': 42, 'p': 41, 's': 44, 'r': 43,
        'u': 46, 't': 45, 'w': 48, 'v': 47, 'y': 50, 'x': 49, 'z': 51,
        }
    result = ''
    while id:
        id, char = id // 64, id % 64
        result += list(alphabet.keys())[list(alphabet.values()).index(char)]
    return 'https://instagram.com/p/' + result[::-1] + '/'

from .node import Node
from .user import User
from funcy import fallback, silent, compose
from .schemas import story_schema
from modeller import Model
from .common import get_image_url, get_manifest, get_video_url
import traceback




# def fallback(*args):
#     first = lambda arr: arr[1:] if len(arr) > 0 else lambda: None
#     rest = lambda arr: arr[:1]if len(arr) > 0 else []
#     return  first(args)() or fallback(rest(args))



class Story(Model, Node):
    _schema = story_schema

    def _on_init(self):
        try:
            self._validate()
        except Exception as e:
            print('ERROR in validation for Story:')
            print()
            print(str(e))
            print()
            print(self._yaml())
            print()


    mpd = property(lambda self: get_manifest(self))

    image = property(lambda self: get_image_url(self))

    image = property(lambda self: get_video_url(self))

    __repr__ = lambda self: f'Story(pk={self.pk})'

    location = property(lambda self: fallback(
        lambda: self['story_locations'][0]['location'],
        lambda: self['story_locations']['location'],
        lambda: None
    ))

    geotag: compose(property, silent)(lambda self: self['story_locations'][0]['location'])

    swipeup_url = property(silent(lambda self: self['story_cta'][0]['links'][0]['webUri']))

    spotyfy_song = property(lambda self: self['story_app_attribution']['content_url'])





"""
{
    id
    latest_reel_media
    expiring_at
    seen
    can_reply
    can_reshare
    reel_type
    user {
        pk
        username
        full_name
        is_private
        profile_pic_url
        profile_pic_id
        friendship_status {
            following
            followed_by
            blocking
            muting
            is_private
            incoming_request
            outgoing_request
            is_bestie
        }
        is_verified
    }
    items[9] {
        taken_at
        pk
        id
        device_timestamp
        media_type
        code
        client_cache_key
        filter_type
        image_versions2 {
            candidates[2] {
                width
                height
                url
            }
        }
        original_width
        original_height
        caption_position
        is_reel_media
        is_dash_eligible
        video_dash_manifest
        video_codec
        number_of_qualities
        video_versions[3] {
            type
            width
            height
            url
            id
        }
        has_audio
        video_duration
        user {
            pk
            username
            full_name
            is_private
            profile_pic_url
            profile_pic_id
            is_verified
            has_anonymous_profile_picture
            reel_auto_archive
            is_unpublished
            is_favorite
        }
        caption {
            _
        }
        caption_is_edited
        photo_of_you
        can_viewer_save
        organic_tracking_token
        expiring_at
        imported_taken_at
        can_reshare
        story_hashtags[1] {
            x
            y
            z
            width
            height
            rotation
            is_pinned
            is_hidden
            hashtag {
                name
                id
            }
        }
        supports_reel_reactions
        show_one_tap_fb_share_tooltip
        has_shared_to_fb
    }
    prefetch_count
    has_besties_media
    media_count
    status
}
"""

from .node import Node
from .user import User
from funcy import fallback
from modeller import Model
import yaml

schema = yaml.load("""
properties:
    ad_action: {}
    attribution:
        properties:
            name:
                type: string
        required:
            - name
        type: object
    can_reply:
        type: boolean
    can_reshare:
        type: boolean
    can_viewer_save:
        type: boolean
    caption:
        type: 'null'
    caption_is_edited:
        type: boolean
    caption_position:
        type: number
    client_cache_key:
        type: string
    code:
        type: string
    creative_config:
        properties:
            camera_facing: {}
            capture_type: {}
            persisted_effect_metadata_json:
                type: string
            should_render_try_it_on: {}
        required:
            - should_render_try_it_on
            - camera_facing
            - capture_type
    device_timestamp:
        type: integer
    expiring_at:
        type: integer
    filter_type:
        type: integer
    has_audio:
        type: boolean
    has_shared_to_fb:
        type: integer
    id:
        type: string
    image_versions2:
        properties:
            candidates:
                properties:
                    height:
                        type: integer
                    url:
                        type: string
                    width:
                        type: integer
                required:
                    - url
                    - height
                    - width
                type: object
        required:
            - candidates
        type: object
    imported_taken_at:
        type: integer
    is_dash_eligible:
        type: integer
    is_reel_media:
        type: boolean
    link_text: {}
    media_type:
        type: integer
    number_of_qualities:
        type: integer
    organic_tracking_token:
        type: string
    original_height:
        type: integer
    original_width:
        type: integer
    photo_of_you:
        type: boolean
    pk:
        type: integer
    reel_mentions:
        properties:
            height:
                type: number
            is_hidden:
                type: integer
            is_pinned:
                type: integer
            rotation:
                type: number
            user:
                properties:
                    full_name:
                        type: string
                    is_private:
                        type: boolean
                    is_verified:
                        type: boolean
                    pk:
                        type: integer
                    profile_pic_id: {}
                    profile_pic_url:
                        type: string
                    username:
                        type: string
                required:
                    - is_private
                    - username
                    - is_verified
                    - pk
                    - full_name
                    - profile_pic_url
                type: object
            width:
                type: number
            x:
                type: number
            y:
                type: number
            z:
                type: integer
        required:
            - height
            - user
            - y
            - width
            - x
            - rotation
            - is_hidden
            - is_pinned
            - z
        type: object
    show_one_tap_fb_share_tooltip:
        type: boolean
    story_countdowns:
        properties:
            countdown_sticker:
                properties:
                    attribution:
                        type: 'null'
                    countdown_id:
                        type: integer
                    digit_card_color:
                        type: string
                    digit_color:
                        type: string
                    end_background_color:
                        type: string
                    end_ts:
                        type: integer
                    following_enabled:
                        type: boolean
                    is_owner:
                        type: boolean
                    start_background_color:
                        type: string
                    text:
                        type: string
                    text_color:
                        type: string
                    viewer_is_following:
                        type: boolean
                required:
                    - attribution
                    - countdown_id
                    - digit_card_color
                    - digit_color
                    - end_background_color
                    - end_ts
                    - following_enabled
                    - is_owner
                    - start_background_color
                    - text
                    - text_color
                    - viewer_is_following
                type: object
            height:
                type: number
            is_hidden:
                type: integer
            is_pinned:
                type: integer
            rotation:
                type: number
            width:
                type: number
            x:
                type: number
            y:
                type: number
            z:
                type: integer
        required:
            - countdown_sticker
            - height
            - is_hidden
            - is_pinned
            - rotation
            - width
            - x
            - y
            - z
        type: object
    story_cta:
        properties:
            felix_deep_link:
                type: string
            links:
                properties:
                    androidClass: {}
                    appInstallObjectiveInvalidationBehavior: {}
                    callToActionTitle: {}
                    deeplinkUri: {}
                    igUserId: {}
                    leadGenFormId: {}
                    linkType: {}
                    package: {}
                    redirectUri: {}
                    webUri: {}
                required:
                    - redirectUri
                    - linkType
                    - deeplinkUri
                    - igUserId
                    - webUri
                    - appInstallObjectiveInvalidationBehavior
                    - leadGenFormId
                    - package
                    - callToActionTitle
                    - androidClass
        required:
            - felix_deep_link
            - links
    story_hashtags:
        properties:
            attribution:
                type: string
            custom_title:
                type: string
            hashtag:
                properties:
                    id: {}
                    name: {}
                required:
                    - id
                    - name
            height: {}
            is_hidden: {}
            is_pinned: {}
            rotation: {}
            width: {}
            x: {}
            y: {}
            z: {}
        required:
            - hashtag
            - height
            - y
            - width
            - x
            - rotation
            - is_hidden
            - is_pinned
            - z
    story_locations:
        properties:
            height:
                type: number
            is_hidden:
                type: integer
            is_pinned:
                type: integer
            location:
                properties:
                    address:
                        type: string
                    city:
                        type: string
                    external_source:
                        type: string
                    facebook_places_id:
                        type: integer
                    lat:
                        type: number
                    lng:
                        type: number
                    name:
                        type: string
                    pk:
                        type: integer
                    short_name:
                        type: string
                required:
                    - city
                    - facebook_places_id
                    - lat
                    - lng
                    - pk
                    - short_name
                    - name
                    - external_source
                    - address
                type: object
            rotation:
                type: number
            width:
                type: number
            x:
                type: number
            y:
                type: number
            z:
                type: integer
        required:
            - height
            - y
            - width
            - location
            - rotation
            - x
            - is_hidden
            - is_pinned
            - z
        type: object
    story_music_stickers:
        properties:
            display_type:
                type: string
            height:
                type: number
            is_hidden:
                type: integer
            is_pinned:
                type: integer
            music_asset_info:
                properties:
                    audio_asset_id:
                        type: string
                    audio_asset_start_time_in_ms:
                        type: integer
                    cover_artwork_thumbnail_uri:
                        type: string
                    cover_artwork_uri:
                        type: string
                    dash_manifest:
                        type: string
                    display_artist:
                        type: string
                    highlight_start_times_in_ms:
                        items:
                            type: integer
                        type: array
                    id:
                        type: string
                    ig_artist: {}
                    overlap_duration_in_ms:
                        type: integer
                    placeholder_profile_pic_url:
                        type: string
                    progressive_download_url:
                        type: string
                    should_mute_audio:
                        type: boolean
                    should_mute_audio_reason:
                        type: string
                    title:
                        type: string
                required:
                    - audio_asset_id
                    - audio_asset_start_time_in_ms
                    - cover_artwork_thumbnail_uri
                    - cover_artwork_uri
                    - dash_manifest
                    - display_artist
                    - highlight_start_times_in_ms
                    - id
                    - ig_artist
                    - is_explicit
                    - overlap_duration_in_ms
                    - placeholder_profile_pic_url
                    - progressive_download_url
                    - should_mute_audio
                    - should_mute_audio_reason
                    - title
                type: object
            rotation:
                type: number
            width:
                type: number
            x:
                type: number
            y:
                type: number
            z:
                type: integer
        required:
            - display_type
            - height
            - is_hidden
            - is_pinned
            - music_asset_info
            - rotation
            - width
            - x
            - y
            - z
        type: object
    story_sliders:
        properties:
            height: {}
            is_hidden: {}
            is_pinned: {}
            rotation: {}
            slider_sticker:
                properties:
                    background_color: {}
                    emoji: {}
                    question: {}
                    slider_id: {}
                    slider_vote_average: {}
                    slider_vote_count: {}
                    text_color: {}
                    viewer_can_vote: {}
                required:
                    - text_color
                    - background_color
                    - question
                    - emoji
                    - slider_id
                    - slider_vote_count
                    - viewer_can_vote
                    - slider_vote_average
            width: {}
            x: {}
            y: {}
            z: {}
        required:
            - height
            - y
            - width
            - x
            - rotation
            - is_hidden
            - is_pinned
            - slider_sticker
            - z
    supports_reel_reactions:
        type: boolean
    taken_at:
        type: integer
    user:
        properties:
            full_name:
                type: string
            has_anonymous_profile_picture:
                type: boolean
            is_favorite:
                type: boolean
            is_private:
                type: boolean
            is_unpublished:
                type: boolean
            is_verified:
                type: boolean
            pk:
                type: integer
            profile_pic_id:
                type: string
            profile_pic_url:
                type: string
            reel_auto_archive:
                type: string
            username:
                type: string
        required:
            - is_private
            - is_unpublished
            - username
            - is_favorite
            - is_verified
            - has_anonymous_profile_picture
            - reel_auto_archive
            - pk
            - profile_pic_id
            - full_name
            - profile_pic_url
        type: object
    video_codec:
        type: string
    video_dash_manifest:
        type: string
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
required:
    - show_one_tap_fb_share_tooltip
    - caption_is_edited
    - client_cache_key
    - has_shared_to_fb
    - original_height
    - can_viewer_save
    - filter_type
    - code
    - original_width
    - caption_position
    - expiring_at
    - media_type
    - organic_tracking_token
    - device_timestamp
    - photo_of_you
    - can_reshare
    - user
    - supports_reel_reactions
    - pk
    - image_versions2
    - caption
    - taken_at
    - can_reply
    - is_reel_media
    - id

""")








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

class Story(Node, Model):
    _schema = schema

    source = property(lambda self: get_url(self))

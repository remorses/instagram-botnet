from .node import Node
from .common import attributes


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



class Story(Node):

    def __init__(self, *, generic=None, id=None, data=None,):
        self._id = id
        self._data = data

        if generic:
            self._data = generic

    def __repr__(self):
            url = self.get_url()
            return 'Story(id=\'{}\', url=\'{}\')'.format(self._id, url)

    def get_data(self, bot):
        return self._data

    def get_expiring_at(self):
        data = self._data
        if 'expiring_at' in data:
            return data['expiring_at']
        else:
            return None

    def get_taken_at(self):
        data = self._data
        if 'taken_at' in data:
            return data['taken_at']
        else:
            return None

    def get_url(self):
        data = self._data
        if 'video_versions' and 'video_duration' in data:
            return data['video_versions'][0]['url']
        elif 'image_versions2' in data:
            return data['image_versions2']['candidates'][0]['url']
        else:
            return None

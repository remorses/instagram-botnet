from .node import Node
import yaml
from modeller import Model

schema = yaml.load("""
properties:
    friendship_status:
        properties:
            blocking:
                type: boolean
            incoming_request:
                type: boolean
            is_private:
                type: boolean
            following:
                type: boolean
            outgoing_request:
                type: boolean
        required:
            - incoming_request
            - following
            - outgoing_request
            - blocking
        type: object
    full_name:
        type: string
    has_anonymous_profile_picture: {}
    is_directapp_installed:
        type: boolean
    is_favorite: {}
    is_private:
        type: boolean
    is_unpublished:
        type: boolean
    is_verified:
        type: boolean
    latest_reel_media:
        type: integer
    pk:
        type: integer
    profile_pic_id:
        type: string
    profile_pic_url:
        type: string
    reel_auto_archive: {}
    username:
        type: string
required:
    - is_private
    - username
    - is_verified
    - pk
    - full_name
    - profile_pic_url
""")

class User(Node, Model):
    _schema = schema
    id = property(lambda self: self['pk'])

from .node import Node
from modeller import Model
import yaml

schema = yaml.load("""
properties:
    bit_flags:
        type: integer
    comment_like_count:
        type: integer
    content_type:
        type: string
    created_at:
        type: integer
    created_at_utc:
        type: integer
    did_report_as_spam:
        type: boolean
    has_liked_comment:
        type: boolean
    has_translation:
        type: boolean
    media_id:
        type: integer
    parent_comment_id:
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
        properties:
            full_name:
                type: string
            is_private:
                type: boolean
            is_verified:
                type: boolean
            pk:
                type: integer
            profile_pic_id:
                type: string
            profile_pic_url:
                type: string
            username:
                type: string
        required:
            - is_private
            - username
            - is_verified
            - pk
            - profile_pic_id
            - full_name
            - profile_pic_url
        type: object
    user_id:
        type: integer
required:
    - user
    - created_at
    - text
    - did_report_as_spam
    - share_enabled
    - user_id
    - comment_like_count
    - content_type
    - bit_flags
    - has_liked_comment
    - pk
    - status
    - created_at_utc
    - type
    - media_id
""")

class Comment(Node, Model):
    _schema = schema

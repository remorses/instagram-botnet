

from_user = '''
{{ 
  update('users', [
    'instagram',
    'kourtneykardash',
    'kimkardashian',
    'homywankenobi',
    'justgabbo',
  ])
}}
---
actions:
  - name: followers
    nodes: {{ data.users }}
    from: user
    edges:
      - type: followers
        amount: 4
      - type: scrape
        key: followers
        model: x.username
  - name: following
    nodes: {{ data.users }}
    from: user
    edges:
      - type: following
        amount: 4
      - type: scrape
        key: following
        model:
          username: x.username
          pk: x.pk
  - name: user_feed
    nodes: {{ data.users }}
    from: user
    edges:
      - type: feed
        amount: 4
      - type: scrape
        key: user_feed
        model: 
          url: x.url
          author: x.user
  - name: stories
    nodes: {{ data.users }}
    from: user
    edges:
      - type: stories
        amount: 4
      - type: scrape
        key: stories
        model:
          image: x.image
          video: x.video
          mpd: x.mpd
          location: x.location
'''

from_media = '''
{{ 
  update('urls', [
    'https://www.instagram.com/p/B0WpFNdg40t/',
    'https://www.instagram.com/p/B0_hdlxgswX/',
    'https://www.instagram.com/p/B0yO5wID0Ne/',
    'https://www.instagram.com/p/BwADod2HnJ_/',
    'https://www.instagram.com/p/BtdloYFnNKR/',
  ])
}}
---
actions:
  - name: likers
    nodes: {{ data.urls }}
    from: media
    edges:
      - type: likers
        amount: 4
      - type: scrape
        key: likers
        model: x.username
  - name: author
    nodes: {{ data.urls }}
    from: media
    edges:
      - type: author
      - type: scrape
        key: author
        model: x.username
  - name: hashtags
    nodes: {{ data.urls }}
    from: media
    edges:
      - type: hashtags
      - type: scrape
        key: hashtags
        model: x.name
  - name: geotag
    nodes: {{ data.urls }}
    from: media
    edges:
      - type: geotag
      - type: scrape
        key: geotag
        model:
          id: x.id
          lat: x.lat
          lng: x.lng
          name: x.name
'''

interactions = '''
actions:
  - name: follow
    nodes: [instagram]
    from: user
    edges:
      - type: feed
        amount: 1
      - type: likers
        amount: 4
      - type: follow
  - name: like
    nodes: [instagram]
    from: user
    edges:
      - type: feed
        amount: 4
      - type: like
  - name: unfollow
    node: [{{ data.username }}]
    from: user
    edges:
      - type: unfollow
        max: 4
  - name: message
    node: [xmorse_]
    from: user
    edges:
      - type: message
        messages:
          - ['ciao', 'heyyy']
          - ['sto testando', 'sto schiumando']
'''


utilities = '''
actions:
  - name: shuffle
    nodes: [instagram]
    from: user
    edges:
      - type: followers
        amount: 6
      - type: print
        expr: x.username
      - type: shuffle
        batch: 3
      - type: print
        expr: x.username
  - name: sleep
    nodes: [instagram]
    from: user
    edges:
      - type: following
        amount: 6
      - type: sleep
        seconds: 1
'''

filters = '''
actions:
  - name: filter
    nodes: [instagram]
    from: user
    edges:
      - type: followers
        amount: 20
      - type: filter
        user:
          follower_count: x < 100
          following_count: x < 100
          is_private: not x
          is_verified: not x
          has_anonymous_profile_picture: not x
          media_count: x < 100
      - type: scrape
        key: filtered
        model:
          username: x.username
          follower_count: x.follower_count
          following_count: x.following_count
          is_private: x.is_private
          is_verified: x.is_verified
          anonymous: x.has_anonymous_profile_picture
          media_count: x.media_count
'''


all = {k:v for k,v in globals().items() if not k.startswith('_')}
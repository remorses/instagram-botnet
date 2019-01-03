from .node import Node
from .common import attributes

"""
	pk
	name
	address
	city
	short_name
	lng
	lat
	external_source
	facebook_places_id
"""

"""
    "pk": 186886085560507,
    "name": "Kartepe",
    "address": "",
    "city": "",
    "short_name": "Kartepe",
    "lng": 30.195368,
    "lat": 40.675953,
    "external_source": "facebook_places",
    "facebook_places_id": 186886085560507
"""

class Geotag(Node):

    def __init__(self, *, generic=None, name=None, id=None, facebook_id=None, lng=None, lat=None, data=None):

        self._name = name
        self._id = id
        self._data = data
        self._facebook_id = facebook_id
        self._lng = lng
        self._lat = lat


        if generic:
            self._name = generic

    def __repr__(self):
        name, id, *_ = attributes(self)

        if name:
            return 'Geotag(name=\'{}\')'.format(name)
        elif id:
            return 'Geotag(id=\'{}\')'.format(id)
        else:
            return 'Geotag(...)'

    @property
    def name(self):
        name, id, data, *_ = attributes(self)

        if name:
            return name
        elif data:
            return data['name']
        else:
            return False

    @property
    def id(self):
        name, id, data, *_ = attributes(self)
        if id:
            return id
        elif data:
            return data['pk']
        else:
            return False

    def get_id(self, bot):
        name, id, _, fb_id, *_ = attributes(self)
        if id:
            return id
        elif fb_id:
            return fb_id
        elif name:
            try:
                bot.api.search_location(name)
                data = bot.last['items'][0]['location']
                return data['pk']
            except TypeError:
                return False
        else:
            return False

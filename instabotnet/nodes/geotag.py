from .node import Node

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
    __slots__ = ['_name', '_id', '_data']
    def __init__(self, *, generic=None, name=None, id=None, data=None):

        self._name = name
        self._id = id
        self._data = data

        if generic:
            self._name = generic

    def __repr__(self):
        name, id, data = attributes(self)

        if name:
            return 'Geotag(name=\'{}\')'.format(name)
        elif id:
            return 'Geotag(id=\'{}\')'.format(id)
        else:
            return 'Geotag(...)'

    @property
    def name(self):
        name, id, data = attributes(self)

        if name:
            return name
        elif data:
            return data['name']
        else:
            return False

    @property
    def id(self):
        name, id, data = attributes(self)
        if id:
            return id
        elif data:
            return data['pk']
        else:
            return False

    def get_data(self, bot):
        name, id, data = attributes(self)
        if data:
            if 'pk' in data:
                self._id = data['pk']
                return self.get_data(bot)
            else:
                return False
        elif name:
            bot.api.search_location(query=name)
            try:
                bot.api.search_location(query=name)
                data = bot.last['items'][0]['location']
                self._data = data
                return data
            except KeyError:
                return False
        elif 'lat' in data and 'lng' in data:
            bot.api.search_location(lat=data['lat'], lng=data['lng'])
            try:
                bot.api.search_location(query=name)
                data = bot.last['items'][0]['location']
                self._data = data
                return data
            except KeyError:
                return False
        else:
            return False


    def get_id(self, bot):
        name, id, data = attributes(self)
        if id:
            return id
        elif data:
            if 'pk' in data:
                return data['pk']
        elif name:
            data = self.get_data(bot)
            return data['pk']
        else:
            return False

    def get_facebook_id(self, bot):
        _, _, data = attributes(self)
        if 'facebook_id' in data:
            return data['facebook_id']
        else:
            data = self.get_data(bot)
            return data['facebook_id']

    def get_coordinates(self, bot):
        _, _, data = attributes(self)
        if 'lat' in data and 'lng' in data:
            return data['lat'], data['lng']
        else:
            data = self.get_data(bot)
            return data['lat'], data['lng']

attributes = lambda x: (x._name, x._id, x._data)

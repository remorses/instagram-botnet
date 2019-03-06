from .node import Node
from funcy import fallback
from modeller import Model
from .schemas import geotag_schema

class Geotag(Node, Model):
    _schema = geotag_schema

    __repr__ = lambda self: f'Geotag(pk={self.id}'

    id = property(lambda self:
        self.pk or \
        self.facebook_places_id or \
        self.external_id or \
        None
    )


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

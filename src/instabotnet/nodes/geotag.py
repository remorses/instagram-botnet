from .node import Node
from funcy import fallback
from modeller import Model
from .schemas import geotag_schema
import traceback

class Geotag(Model, Node):
    _schema = geotag_schema

    def _on_init(self):
        try:
            self._validate()
        except Exception as e:
            print('ERROR in validation for Geotag:')
            print()
            print(str(e))
            print()
            print(self._yaml())
            print()
            
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

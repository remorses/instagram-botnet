from .node import Node
import yaml
from funcy import fallback
from modeller import Model
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

schema = yaml.load("""
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
""")


class Geotag(Node, Model):
    _schema = schema

    id = property(lambda self: fallback(
        lambda: self.pk,
        lambda: self.facebook_places_id,
        lambda: None
    ))

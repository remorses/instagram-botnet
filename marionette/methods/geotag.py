from funcy import rcompose, take
from itertools import islice
from ..nodes import Geotag, Media
from .common import accepts


@accepts(Media)
def geotag(bot, nodes, amount, args) -> Geotag:

    _geotag = rcompose(
        lambda node: node.id,
        lambda id: get_item(bot, id),
    )

    pack_geotag = rcompose(
        lambda data: Geotag(name=data['name'],
                        id=data['pk'],
                        facebook_id=data['facebook_places_id'],
                        lng=data['lng'],
                        lat=data['lat'],
                        data=data
                    )
    )

    result = (pack_geotag(item) for media in nodes for item in _geotag(media))
    result = (geotag for geotag in result if bot.suitable(geotag))
    result = take(amount, result)

    return result, bot.last

def get_item(bot, id):
    """
    data type:
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
    bot.api.media_info(id)
    try:
        item = bot.last["items"][0]["location"]
        yield item
    except TypeError:
        yield from []

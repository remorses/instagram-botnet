

from instabot import API
from pp_json import pp_json
id = 3427797337

api = API()
api.login("***REMOVED***", "***REMOVED***")


api.get_geo_media(id)
result = api.last_json
pp_json(result)

for key in result:
    print("key:", key)

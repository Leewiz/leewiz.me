
from google.transit import gtfs_realtime_pb2
import requests

BDFM_REALTIME_FEED = 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-bdfm'

feed = gtfs_realtime_pb2.FeedMessage()
response = requests.get(BDFM_REALTIME_FEED)
feed.ParseFromString(response.content)
for entity in feed.entity:
    if entity.HasField('trip_update'):
        print(entity.trip_update)
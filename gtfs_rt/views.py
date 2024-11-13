import requests
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import render

from google.transit import gtfs_realtime_pb2

from gtfs_rt.mta_subway_stations import MTA_SUBWAY_STATIONS

###
### makemigration
### import models
### parse mta feed into models
### create models for geojson (subway station data)

BDFMS_REALTIME_URL = 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-bdfm'

@api_view(['GET'])
def hello_world(request):
    print("hello world")
    return render(request, "gtfs_rt/index.html")

@api_view(['GET'])
def get_train_data(request):
    if request.method == 'POST':
        print("POST")
        return render(request, "gtfs_rt/index.html")
    else:
        feed = gtfs_realtime_pb2.FeedMessage()
        response = requests.get(BDFMS_REALTIME_URL)
        feed.ParseFromString(response.content)
        count = 0
        for entity in feed.entity:
            if entity.HasField('trip_update'):
                print("count: ", count)
                count = (count + 1) if (count != 50) else 50
                # print(entity.trip_update)
            if count == 50:
                print("count: ", count)
                print(MTA_SUBWAY_STATIONS)
                count += 1
        print(feed)
        return render(request, "gtfs_rt/index.html")
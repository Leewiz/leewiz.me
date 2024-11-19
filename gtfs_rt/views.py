import requests
from datetime import datetime

from django.utils.timezone import make_aware
from django.shortcuts import render
from rest_framework import generics, permissions, renderers, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from google.transit import gtfs_realtime_pb2

from .models import SubwayEntity, SubwayStation, SubwayStopTimeUpdate
from .serializers import SubwayStationSerializer

###
### makemigration
### import models
### parse mta feed into models
### create models for geojson (subway station data)
### create endpoint to add/update database with fresh data
### create endpoints to query database data using model queryset

BDFMS_REALTIME_URL = 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-bdfm'

def hello_world(request):
    print("hello world")
    return render(request, "gtfs_rt/index.html")

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
            if entity.HasField('trip_update') or entity.HasField('vehicle'):
                if count == 50:
                    for stop in entity.trip_update.stop_time_update:
                        time = datetime.fromtimestamp(stop.arrival.time)
                        tz_aware_time = make_aware(time)
                        print(entity.trip_update.trip.route_id, tz_aware_time, stop.stop_id)
                if count == 49:
                    print(entity)
            count += 1
        return render(request, "gtfs_rt/index.html")
    
# trip_update
#   - stop_time_update
#     - stop_id
#     - arrival
#       - time
#     - departure
#       - time
def get_train(request):
    feed = gtfs_realtime_pb2.FeedMessage()
    response = requests.get(BDFMS_REALTIME_URL)
    feed.ParseFromString(response.content)
    train = SubwayEntity()
    for entity in feed.entity:
        if entity.HasField('trip_update'):
            if entity.trip_update.trip.route_id == 'F':
                train.route_id = entity.trip_update.trip.route_id
                for stop in entity.trip_update.stop_time_update:
                    if "F24" in stop.stop_id:
                        if stop.stop_id[-1] == "N":
                            print(f'stop_id: {stop.stop_id}, arrival_time: {make_aware(datetime.fromtimestamp(stop.arrival.time))}')
    viewFunc = SubwayStationViewSet.as_view({'get': 'boroughs'})
    res = viewFunc(request)
    return render(request, "gtfs_rt/index.html", res.data)
    
class SubwayStationViewSet(viewsets.ModelViewSet):
    """
    this ViewSet automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions
    """
    queryset = SubwayStation.objects.all()
    serializer_class = SubwayStationSerializer
    context_object_name = "subway_stations"
    template_name = "gtfs_rt/index.html"
    renderer_classes = (renderers.JSONRenderer, renderers.TemplateHTMLRenderer)
    
    def retrieve(self, request, *args, **kwargs):
        response = super(SubwayStationViewSet, self).retrieve(request, *args, **kwargs)
        if request.accepted_renderer.format == 'html':
            return Response({'data': response.data}, template_name = self.template_name)
        return response
    
    def list(self, request, *args, **kwargs):
        response = super(SubwayStationViewSet, self).list(request, *args, **kwargs)
        if request.accepted_renderer.format == 'html':
            return Response({'data': response.data}, template_name = self.template_name)
        return response
        
    @action(detail=False, url_path="stations")
    def stations(self, request, *args, **kwargs):
        """
        retrieve a list of unique stop names
        """
        response = super(SubwayStationViewSet, self).list(request, *args, **kwargs)
        if request.accepted_renderer.format == 'html':
            data = self.queryset.values_list("stop_name", flat=True).distinct()
            return Response({'data': self.get_serializer().flatten(data)}, template_name = self.template_name)
        return response
    
    @action(detail=False, url_path="boroughs")
    def boroughs(self, request, *args, **kwargs):
        """
        retrieve a list of boroughs
        """
        response = super(SubwayStationViewSet, self).list(request, *args, **kwargs)
        if request.accepted_renderer.format == 'html':
            data = self.queryset.values_list("borough", flat=True).distinct()
            return Response({'boroughs': self.get_serializer().borough_fullname(data)}, template_name = self.template_name)
        return response
import requests
from datetime import datetime, timedelta

from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.utils.timezone import make_aware
from django.shortcuts import render
from rest_framework import renderers, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from google.transit import gtfs_realtime_pb2
from google.protobuf.json_format import MessageToDict

from .models import SubwayEntity, SubwayStation, StopTimeUpdate
from .serializers import SubwayStationSerializer
from .forms import SubwayForm

### create function to decode stop_ids from feed entities
### parse mta feed into models
### create endpoint to add/update database with fresh data
### create endpoints to query database data using model queryset

BDFMS_REALTIME_URL = 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-bdfm'

# helpers.js calls this endpoint to populate subway dropdown menus
def get_stops(request):
    if 'borough' in request.GET and request.GET['borough']:
        stops =  SubwayStation.objects.filter(borough=request.GET['borough'])
        return JsonResponse(
            {'data': [{'id': stop.gtfs_stop_id, 'stop_name': stop.stop_name } for stop in stops]}
        )
    return JsonResponse({'data': []})

# trip_update
#   - stop_time_update
#     - stop_id
#     - arrival
#       - time
#     - departure
#       - time
from pprint import pprint
def get_times_by_stop_id(request):
    stop_times = {}
    if 'stop_id' in request.GET:
        #stop_times = StopTimeUpdate.objects.filter(stop_id__icontains=)
        ret = []
        count = 0
        for train in next_trains:
            count += 1
            print(f'!!!!!!!!!!!!!{count}!!!!!!!!!!!!!')
            pprint(train.stop_time_updates)
            
        return JsonResponse({'data': ret})
    return JsonResponse({'data': []})

def subway_form(request):
    print('loading form')
    if request.method == "POST":
        form = SubwayForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect("/thanks/")
    
    else:
        form = SubwayForm()
        
    return render(request, "gtfs_rt/selected_stop.html", {"form": form})

def get_train_data(request):
    if request.method == 'POST':
        print("POST")
        return render(request, "gtfs_rt/index.html")
    else:
        '''SubwayEntity
        entity_id = models.CharField(max_length=100)
        trip_id = models.CharField(max_length=100)
        start_time = models.DateTimeField()
        start_date = models.DateTimeField()
        route_id = models.CharField(max_length=100)
        travel_direction = models.CharField(max_length=100)
        stop_time_updates = models.JSonField()

        '''
        '''StopTimeUpdate
        arrival_time = models.DateTimeField()
        departure_time = models.DateTimeField()
        stop_id = models.CharField(max_length=100)
        '''
        feed = gtfs_realtime_pb2.FeedMessage()
        response = requests.get(BDFMS_REALTIME_URL)
        feed.ParseFromString(response.content)
        seent = set()
        keep = []
        print('loading')
        count = 0
        for entity in feed.entity:
            if entity.id in seent:
                print('seent: ', entity.id)
            else:
                seent.add(entity.id)
                keep.append(entity.id)
            
            if entity.HasField('trip_update'):
                subway_entity, created = SubwayEntity.objects.get_or_create(entity_id = entity.id)
                data = MessageToDict(entity.trip_update)
                subway_entity.trip_id = data['trip']['tripId']
                subway_entity.start_time = make_aware(datetime.strptime(data['trip']['startTime'], '%H:%M:%S'))
                subway_entity.start_date = make_aware(datetime.strptime(data['trip']['startDate'], '%Y%m%d'))
                subway_entity.route_id = data['trip']['routeId']
                subway_entity.save()

                stops = data.get('stopTimeUpdate', None)
                if stops:
                    for stop in stops:
                        stop_time_update, created = StopTimeUpdate.objects.get_or_create(
                            subway_entity = subway_entity,
                            stop_id = stop['stopId'],
                            arrival_time = make_aware(datetime.fromtimestamp(int(stop['arrival']['time']))),
                            departure_time = make_aware(datetime.fromtimestamp(int(stop['departure']['time']))),
                        )
                        if not created:
                            count += 1
                            print(f'duplicate {count}: {subway_entity.entity_id} {stop['stopId']} {make_aware(datetime.fromtimestamp(int(stop['arrival']['time'])))}')

        print('done')
        return HttpResponseRedirect(reverse("subway"))

# purge stop_time_updates whose arrival_time has passed by 30 minutes
def purge_old_stop_data(request):
    thirty_minutes_ago = timezone.now() - timedelta(minutes=30)
    StopTimeUpdate.objects.filter(arrival_time__lt=thirty_minutes_ago).delete()
    return HttpResponseRedirect(reverse("subway"))
    
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
            data = self.queryset.values("stop_name", "gtfs_stop_id", "daytime_routes", "borough").distinct()
            return Response({'stations': self.get_serializer().flatten(data)}, template_name = self.template_name)
        return response
    
    @action(detail=False, url_path="boroughs")
    def boroughs(self, request, *args, **kwargs):
        """
        retrieve a list of boroughs
        """
        response = super(SubwayStationViewSet, self).list(request, *args, **kwargs)
        if request.accepted_renderer.format == 'html':
            boroughs = self.queryset.values_list('borough', flat=True).distinct()
            data = self.get_serializer().flatten(boroughs)
            return Response({'boroughs': data }, template_name = self.template_name)
        return response
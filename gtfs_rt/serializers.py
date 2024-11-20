from rest_framework import serializers
from .models import SubwayStation

class SubwayStationSerializer(serializers.HyperlinkedModelSerializer):   
    class Meta:
        model = SubwayStation
        fields = [
            'borough',
            'station_id',
            'stop_name',
            'complex_id',
            'division',
            'north_direction_label',
            'south_direction_label',
            'line',
            'daytime_routes',
            'structure',
            'gtfs_stop_id',
            'gtfs_latitude',
            'gtfs_longitude',
            'ada_notes',
            'ada',
            'ada_northbound',
            'ada_southbound',
            'cbd'
        ]
        
    def flatten(self, obj):
        return SingleField().to_representation(obj)

class SingleField(serializers.Field):
    def to_representation(self, obj):
        return list(obj)
        
            
from rest_framework import serializers
from .models import SubwayStation
        
      
class SubwayStationSerializer(serializers.HyperlinkedModelSerializer):    
    class Meta:
        model = SubwayStation
        fields = [
            'station_id',
            'stop_name',
            'complex_id',
            'division',
            'borough',
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
    
    def borough_fullname(self, obj):
        ret = []
        for borough in obj:
            if borough == 'Q':
                ret.append('Queens')
            elif borough == 'M':
                ret.append('Manhattan')
            elif borough == 'Bk':
                ret.append('Brooklyn')
            elif borough == 'Bx':
                ret.append('Bronx')
            elif borough == 'SI':
                ret.append('Staten Island')
        return ret

class SingleField(serializers.Field):
    def to_representation(self, obj):
        return list(obj)
        
            
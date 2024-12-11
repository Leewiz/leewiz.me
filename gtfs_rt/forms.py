from django import forms
from .models import SubwayStation

ROUTES = [('B', 'B'), ('D', 'D'), ('F', 'F'), ('M', 'M')]

def get_borough_choices():
        choices = SubwayStation.objects.values_list('borough', flat=True).distinct()
        borough_choices = []
        for borough in choices:
            if borough == 'Q':
                borough_choices.append(('Q', 'Queens'))
            elif borough == 'Bk':
                borough_choices.append(('Bk', 'Brooklyn'))
            elif borough == 'Bx':
                borough_choices.append(('Bx', 'Bronx'))
            elif borough == 'M':
                borough_choices.append(('M', 'Manhattan'))
            elif borough == 'SI':
                borough_choices.append(('SI', 'Staten Island'))
        return borough_choices

def get_stop_names_by_route_and_borough(route, borough):
    stops = SubwayStation.objects.filter(daytime_routes__icontains=route, borough=borough).values('gtfs_stop_id', 'stop_name')
    seen = set()
    keep = []
    for stop in stops:
        if stop['stop_name'] in seen:
            print('seent: ', stop['gtfs_stop_id'], stop['stop_name'])
        else:
            seen.add(stop['stop_name'])
            keep.append((stop['gtfs_stop_id'], stop['stop_name']))
    return keep
    
class SubwayForm(forms.ModelForm):
    class Meta:
        model = SubwayStation
        fields = ['daytime_routes', 'borough', 'stop_name']
        labels = {
            'daytime_routes': 'route',
            'borough': 'borough',
            'stop_name': 'stop name',
        }
        widgets = {
            # these onchange functions can be found in helerps.js
            'daytime_routes': forms.Select(attrs={'onchange': 'get_stops_by_borough();'}),
            'borough': forms.Select(attrs={'onchange': 'get_stops_by_borough();'}),
            'stop_name': forms.Select(attrs={'onchange': 'get_time_to_next_train(this.value);'})
        }
        
    def __init__(self, *args, **kwargs):
        super(SubwayForm, self).__init__(*args, **kwargs)
        # populate select widgets with unique choices for borough and stop_name
        boroughs = get_borough_choices()
        routes = ROUTES
        self.fields['daytime_routes'].widget.choices = routes
        self.fields['daytime_routes'].widget.initial = routes[0]
        self.fields['borough'].widget.choices = boroughs
        self.fields['borough'].initial = boroughs[0]
        stops = get_stop_names_by_route_and_borough(routes[0], boroughs[0][0])
        self.fields['stop_name'].widget.choices = stops
        

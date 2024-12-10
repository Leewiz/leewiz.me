from django import forms
from .models import SubwayStation

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

def get_stop_names_by_borough(borough):
    stops = SubwayStation.objects.filter(borough=borough).values('gtfs_stop_id', 'stop_name')
    seen = set()
    keep = []
    for stop in stops:
        if stop['stop_name'] in seen:
            seen
            #print('seent: ', stop['gtfs_stop_id'], stop['stop_name'])
        else:
            seen.add(stop['stop_name'])
            keep.append((stop['gtfs_stop_id'], stop['stop_name']))
    return keep
    
class SubwayForm(forms.ModelForm):
    class Meta:
        model = SubwayStation
        fields = ['borough', 'stop_name']
        labels = {
            'borough': 'borough',
            'stop_name': 'stop name',
        }
        widgets = {
            'borough': forms.Select(attrs={'onchange': 'get_stops_by_borough(this.value);'}),
            'stop_name': forms.Select(attrs={'onchange': 'get_time_to_next_train(this.value);'})
        }
        
    def __init__(self, *args, **kwargs):
        super(SubwayForm, self).__init__(*args, **kwargs)
        # populate select widgets with unique choices for borough and stop_name
        boroughs = get_borough_choices()
        self.fields['borough'].widget.choices = boroughs
        self.fields['borough'].initial = boroughs[0]
        stops = get_stop_names_by_borough(boroughs[0][0])
        self.fields['stop_name'].widget.choices = stops
        

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

class SubwayForm(forms.ModelForm):
    class Meta:
        model = SubwayStation
        fields = ['borough', 'stop_name']
        labels = {
            'borough': 'borough',
            'stop_name': 'stop name',
        }
        widgets = {
            'borough': forms.Select(attrs={'onchange': 'get_stops_by_borough(this.value);'}, choices=get_borough_choices()),
            'stop_name': forms.Select()
        }


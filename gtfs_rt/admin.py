from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import SubwayStation, SubwayEntity, StopTimeUpdate

class StopTimeUpdateInline(admin.TabularInline):
    model = StopTimeUpdate

class SubwayStationAdmin(admin.ModelAdmin):
    list_filter = ["stop_name"]
    search_fields = ["gtfs_stop_id", "stop_name", "borough"]
    list_display = ["gtfs_stop_id", "station_id", "stop_name", "borough"]

class SubwayEntityAdmin(admin.ModelAdmin):
    list_filter = ["entity_id"]
    search_fields = ["route_id"]
    list_display = ["entity_id", "trip_id", "route_id", "start_date"]
    
class StopTimeUpdateAdmin(admin.ModelAdmin):
    list_filter = ["subway_entity"]
    search_fields = ["stop_id", "arrival_time"]
    list_display = ["stop_id", "arrival_time", "departure_time", "subway_entity_link"]
    
    def subway_entity_link(self, obj):
        url = reverse('admin:gtfs_rt_subwayentity_change', args=(obj.subway_entity.id,))
        return mark_safe(f'<a href="{url}">{obj.subway_entity.entity_id}</a>')
    

admin.site.register(SubwayStation, SubwayStationAdmin)
admin.site.register(SubwayEntity, SubwayEntityAdmin)
admin.site.register(StopTimeUpdate, StopTimeUpdateAdmin)

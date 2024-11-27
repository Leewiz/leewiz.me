from django.contrib import admin

from .models import SubwayStation, SubwayEntity


class SubwayStationAdmin(admin.ModelAdmin):
    list_filter = ["stop_name"]
    search_fields = ["stop_name", "borough"]
    list_display = ["station_id", "stop_name", "borough"]

class SubwayEntityAdmin(admin.ModelAdmin):
    list_filter = ["entity_id"]
    list_display = ["entity_id", "trip_id", "route_id", "start_date"]
    
admin.site.register(SubwayStation, SubwayStationAdmin)
admin.site.register(SubwayEntity, SubwayEntityAdmin)

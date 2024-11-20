from django.contrib import admin

from .models import SubwayStation

class SubwayStationAdmin(admin.ModelAdmin):
    list_filter = ["stop_name"]
    search_fields = ["stop_name", "borough"]
    list_display = ["station_id", "stop_name", "borough"]
       
admin.site.register(SubwayStation, SubwayStationAdmin)

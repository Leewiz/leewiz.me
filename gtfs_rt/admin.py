from django.contrib import admin

from .models import SubwayStation

class SubwayStationAdmin(admin.ModelAdmin):
    list_filter = ["stop_name"]
    search_fields = ["stop_name", "borough"]
    list_display = ["station_id", "stop_name", "borough"]
    # fieldsets = [
    #     (None, {"fields": ["stop_name"]}),
    #     ("date information", {"fields": ["pub_date"], "classes": ["collapse"]}),
    # ]
    
admin.site.register(SubwayStation, SubwayStationAdmin)

    # station_id = models.CharField(max_length=10)
    # stop_name = models.CharField(max_length=100)
    # complex_id = models.CharField(max_length=100)
    # division = models.CharField(max_length=100)
    # borough = models.CharField(max_length=100)
    # north_direction_label = models.CharField(max_length=100)
    # south_direction_label = models.CharField(max_length=100)
    # line = models.CharField(max_length=100)
    # daytime_routes = models.CharField(max_length=100)
    # structure = models.CharField(max_length=100)
    # gtfs_stop_id = models.CharField(max_length=100)
    # gtfs_latitude = models.CharField(max_length=100)
    # gtfs_longitude = models.CharField(max_length=100)
    # ada_notes = models.CharField(max_length=100, null=True)
    # ada = models.CharField(max_length=100)
    # ada_northbound = models.CharField(max_length=100)
    # ada_southbound = models.CharField(max_length=100)
    # cbd = models.CharField(max_length=100)

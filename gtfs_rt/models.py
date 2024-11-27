from django.db import models
    
'''
display idea:
dropdown for route id (BDFMS)
   - populate dropdown with stations on route
   - display next scheduled train in each direction
'''

class SubwayEntity(models.Model):
    # entity_id
    # route name (B, D, F, M, etc)
    # travel direction
    # SubwayTrip (one-to-many)
    # SubwayStopTimeUpdate (many-to-many)
    
    entity_id = models.CharField(max_length=100)
    trip_id = models.CharField(max_length=100)
    start_time = models.TimeField(null=True)
    start_date = models.DateField(null=True)
    route_id = models.CharField(max_length=100)
    travel_direction = models.CharField(max_length=100)
    stop_time_updates = models.JSONField(null=True)

class SubwayStation(models.Model):
    station_id = models.CharField(max_length=10)
    borough = models.CharField(max_length=100)
    stop_name = models.CharField(max_length=100)
    complex_id = models.CharField(max_length=100)
    division = models.CharField(max_length=100)
    north_direction_label = models.CharField(max_length=100)
    south_direction_label = models.CharField(max_length=100)
    line = models.CharField(max_length=100)
    daytime_routes = models.CharField(max_length=100)
    structure = models.CharField(max_length=100)
    gtfs_stop_id = models.CharField(max_length=100, unique=True)
    gtfs_latitude = models.CharField(max_length=100)
    gtfs_longitude = models.CharField(max_length=100)
    ada_notes = models.CharField(max_length=100, null=True)
    ada = models.CharField(max_length=100)
    ada_northbound = models.CharField(max_length=100)
    ada_southbound = models.CharField(max_length=100)
    cbd = models.CharField(max_length=100)
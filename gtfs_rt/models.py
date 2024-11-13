from django.db import models
    
class SubwayStopTimeUpdate(models.Model):
    arrival_time = models.DateTimeField()
    departure_time = models.DateTimeField()
    stop_id = models.CharField(max_length=100)

class SubwayEntity(models.Model):
    # entity_id
    # route name (B, D, F, M, etc)
    # travel direction
    # SubwayTrip (one-to-many)
    # SubwayStopTimeUpdate (many-to-many)
    
    entity_id = models.CharField(max_length=100)
    trip_id = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    start_date = models.DateTimeField()
    route_id = models.CharField(max_length=100)
    travel_direction = models.CharField(max_length=100)
    stop_time_updates = models.ManyToManyField(SubwayStopTimeUpdate)

import json

with open('gtfs_rt/mta_subway_stations.geojson') as f:
    MTA_SUBWAY_STATIONS = json.load(f)


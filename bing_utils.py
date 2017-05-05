import constants
import requests
import json

def get_traffic_data(lat, lon):
    # 10001.965729km = 90 degrees
    # 1km = 90/10001.965729 degrees = 0.0089982311916 degrees
    # 10km = 0.089982311915998 degrees
    lat = -33.8591
    lon = 151.2002
    south_lat = str(lat - 0.08999)
    west_lon = str(lon - 0.08999)
    north_lat = str(lat + 0.08999)
    east_lon = str(lon + 0.08999)
    traffic_request = requests.get('http://dev.virtualearth.net/REST/v1/Traffic/Incidents/{},{},{},{}?key={}'
                                   .format(south_lat, west_lon, north_lat, east_lon, constants.BING_MAPS_KEY))
    traffic_json = traffic_request.json()
    return traffic_json

get_traffic_data()
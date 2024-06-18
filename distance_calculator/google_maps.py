import googlemaps
from distance_calculator.settings import GOOGLE_MAPS_API_KEY

gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)

def get_geocode(address):
    geocode_result = gmaps.geocode(address)
    if geocode_result:
        return geocode_result
    return None

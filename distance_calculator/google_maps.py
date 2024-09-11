import googlemaps
import logging
from dotenv import load_dotenv
import os

load_dotenv()

GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')
gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)

def get_geocode(address):
    try:
        geocode_result = gmaps.geocode(address)
        if not geocode_result:
            raise ValueError("No results found for the address.")
        return geocode_result
    except googlemaps.exceptions.ApiError as e:
        logging.error(f"API Error: {e}")
        raise
    except googlemaps.exceptions.TransportError as e:
        logging.error(f"Transport Error: {e}")
        raise
    except googlemaps.exceptions.Timeout as e:
        logging.error(f"Timeout Error: {e}")
        raise
    except googlemaps.exceptions._OverQueryLimit as e:
        logging.error(f"Over Query Limit Error: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise

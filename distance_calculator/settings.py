import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_MAPS_API_KEY = "AIzaSyA75_gIkupDOHd64HUstBz_vQ_VVV6C5Os"


DB_CONFIG = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'AccommodationDB',
        'USER': 'root',
        'PASSWORD': '98Naturena!!',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}


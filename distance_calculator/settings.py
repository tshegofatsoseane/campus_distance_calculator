import os
from dotenv import load_dotenv


load_dotenv()

GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'AccommodationDB',
        'USER': 'root',
        'PASSWORD': '98Naturena!!',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
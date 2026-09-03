#import all settings data from the base.py(original settings)
from .base import *
#we only need to take Debug and database
DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
import os

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'mptt',
    'easy_thumbnails',
    'sekizai',
    'smartsnippets',
    'cms',
    'filer',
    'cmsplugin_image',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME' : 'test.db', # Or path to database file if using sqlite3.
        'USER' : '', # Not used with sqlite3.
        'PASSWORD' : '', # Not used with sqlite3.
        'HOST' : '', # Set to empty string for localhost. Not used with sqlite3.
        'PORT' : '', # Set to empty string for default. Not used with sqlite3.
    }
}

ROOT_URLCONF = 'cmsplugin_image.tests.urls'
HERE = os.path.dirname(os.path.realpath(__file__))
MEDIA_ROOT = os.path.abspath( os.path.join(HERE, 'media') )
MEDIA_URL = '/media/'
STATIC_URL = '/static/'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
)
SECRET_KEY = 'secret'
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)
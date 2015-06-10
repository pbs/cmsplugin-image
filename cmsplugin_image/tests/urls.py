from django.conf.urls import *

urlpatterns = patterns('cmsplugin_image.views',
    (r'^imagefield/get_file/', 'get_file'),
)

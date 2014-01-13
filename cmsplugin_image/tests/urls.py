from django.conf.urls.defaults import *

urlpatterns = patterns('cmsplugin_image.views',
    (r'^imagefield/get_file/', 'get_file'),
)

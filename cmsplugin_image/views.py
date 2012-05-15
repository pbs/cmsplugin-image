from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from filer.models import File, Folder

try:
    import json
except:
    import simplejson as json


@login_required
def get_file(request):
    if not request.is_ajax():
        return HttpResponseForbidden()
    file_id = request.GET.get('id');
    try:
        file = File.objects.get(pk=file_id).file.url
    except File.DoesNotExist:
        file = None    
    return HttpResponse(json.dumps(file), mimetype="application/json")

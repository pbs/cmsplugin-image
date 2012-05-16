from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from filer.models import File, Image

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
        file = File.objects.get(pk=file_id)
    except File.DoesNotExist:
        file = None
    if file and file.__class__ == Image:
        return HttpResponse(json.dumps(file.file.url), mimetype="application/json")
    return HttpResponse(json.dumps(None), mimetype="application/json")
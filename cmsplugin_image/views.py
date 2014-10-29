from django.contrib.auth.decorators import login_required
from django.http import (
    HttpResponse, HttpResponseForbidden, HttpResponseBadRequest)
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
    try:
        file_id = int(request.GET.get('id', None))
    except (TypeError, ValueError):
        return HttpResponseBadRequest('Filer file missing or not a number')

    file_type = (request.GET.get('file_type') or 'image').lower()
    available_models = {
        'image': Image,
        'file': File
    }
    model = available_models.get(file_type)
    if not model:
        return HttpResponseBadRequest("File type not available.")

    filer_object = get_object_or_404(model, id=file_id)
    file_url = filer_object.file.url

    return HttpResponse(
        json.dumps({'url': file_url}), mimetype="application/json")

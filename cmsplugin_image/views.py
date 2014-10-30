from django.contrib.auth.decorators import login_required
from django.http import (
    HttpResponse, HttpResponseForbidden, HttpResponseBadRequest, Http404)
from cmsplugin_image.widgets import FILER_WIDGETS
from filer.models import File

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

    file_type = (
        request.GET.get('file_type') or 'image'
    ).strip().lower()

    if file_type not in [widget.filer_file_type for widget in FILER_WIDGETS]:
        return HttpResponseBadRequest('File type not available.')

    try:
        filer_object = File.objects.get(id=file_id)
    except File.DoesNotExist:
        raise Http404

    filer_object_type = filer_object.file_type.lower()

    is_image = file_type == filer_object_type == 'image'
    # allow all other file types different than image since we don't have
    #   an archive snippet field yet
    is_file = file_type == 'file' and filer_object_type != 'image'
    file_url = filer_object.file.url if is_image or is_file else ""

    return HttpResponse(
        json.dumps({'url': file_url}), mimetype="application/json")

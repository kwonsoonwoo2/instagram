import os

from django.conf import settings
from django.http import HttpResponse, FileResponse


def media_serve(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)

    return FileResponse(open(file_path, 'rb'), content_type='image/jpeg')
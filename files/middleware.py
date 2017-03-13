from django.conf import settings

from files.models import File, FileDownloadLog


class FileStatMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        if response.status_code != 404 and request.get_full_path().startswith(settings.MEDIA_URL):
            file = File.objects.get(file=request.get_full_path().replace(settings.MEDIA_URL, ''))
            FileDownloadLog.objects.create(file = file)

        # Code to be executed for each request/response after
        # the view is called.

        return response
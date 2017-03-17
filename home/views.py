from django.views.generic import ListView
from django.http import HttpResponse
from files.models import File
from django.db import models


class FeedView(ListView):
    template_name = 'home/feed.html'
    checked_files_ids = list()
    queryset = File.objects.all()

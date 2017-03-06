from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.views.generic import CreateView
from django.views.generic import ListView

from files.models import File


class FileList(ListView):
    queryset = File.objects.all()
    template_name = 'files/list.html'


class FileUpload(CreateView):
    model = File
    fields = ['file', 'name', 'course']
    template_name = 'files/upload.html'
    def get_success_url(self):
        return reverse('file-list')
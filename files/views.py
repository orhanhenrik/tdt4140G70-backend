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

    def get_context_data(self, **kwargs):
        context = super(Browse, self).get_context_data(**kwargs)
        all_names = File.objects.values_list('name')
        all_types = set()
        for name in all_names:
            type = name[name.index('.'):]
            all_types.add(type)
        context["file_types_list"] = all_types
        return context

    def get_queryset(self):
        filetype = self.request.GET.get("filetype_choice")
        if filetype == "" or filetype == null:
            queryset = File.objects.all()
        else:
            queryset = File.objects.all().filter(name__endswith=filetype)
        return queryset


class FileUpload(CreateView):
    model = File
    fields = ['file', 'name', 'course']
    template_name = 'files/upload.html'

    def get_success_url(self):
        return reverse('file-list')

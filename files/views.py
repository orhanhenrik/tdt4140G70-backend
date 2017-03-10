from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.views.generic import CreateView
from django.views.generic import ListView
from django.http.response import HttpResponse
from files.models import File


class FileList(ListView):
    # permission_classes = (permissions.AllowAny,)
    queryset = File.objects.all()
    template_name = 'files/list.html'
    checked_files_ids = list()

    def get_context_data(self, **kwargs):
        context = super(FileList, self).get_context_data(**kwargs)
        all_files = File.objects.all()
        all_types = set()
        for file in all_files:
            name = file.filename()
            type = name[(name.index('.') + 1):]
            all_types.add(type)
        context["filetype"] = self.request.GET.get("filetype_choice")
        context["file_types_list"] = all_types

        self.checked_files_ids = self.request.GET.getlist('checks[]')
        return context

    def get_queryset(self):
        filetype = self.request.GET.get("filetype_choice")
        if filetype == "All" or filetype is None:
            queryset = File.objects.all()
        else:
            queryset = File.objects.all().filter(file__endswith=filetype)
        return queryset

    # def post(self, request, format=None):
    #     return HttpResponse("ok")


class FileUpload(CreateView):
    dialog_count = 1
    model = File
    fields = ['file', 'name', 'course']
    template_name = 'files/upload.html'

    def get_context_data(self, **kwargs):
        context = super(FileUpload, self).get_context_data(**kwargs)
        context["range"] = range(self.dialog_count)
        return context

    def get_success_url(self):
        return reverse('file-list')

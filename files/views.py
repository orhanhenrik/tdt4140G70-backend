from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.views.generic import CreateView
from django.views.generic import ListView
from django.http import HttpResponse
from files.models import File

from io import StringIO
from io import BytesIO
import zipfile
import os


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

        return context

    def get_queryset(self):
        filetype = self.request.GET.get("filetype_choice")
        if filetype == "All" or filetype is None:
            queryset = File.objects.all()
        else:
            queryset = File.objects.all().filter(file__endswith=filetype)
        return queryset

    def get(self, request, format=None):
        self.checked_files_ids = self.request.GET.getlist('checks[]')

        if self.checked_files_ids:

            checked_files = list()
            for file_id in self.checked_files_ids:
                checked_files.append(File.objects.get(id=file_id))

            checked_filenames = list()
            for file in checked_files:
                checked_filenames.append(file.file.path)

            zip_subdir = "crawlingfiles"
            zip_filename = "%s.zip" % zip_subdir

            # Open StringIO to grab in-memory ZIP contents
            s = BytesIO()

            # The zip compressor
            zf = zipfile.ZipFile(s, "w")

            for fpath in checked_filenames:
                # Calculate path for file in zip
                fdir, fname = os.path.split(fpath)
                zip_path = os.path.join(zip_subdir, fname)

                # print(zip_path, zip_subdir, fpath)
                # Add file, at correct path
                zf.write(fpath, zip_path)

            # Must close zip for all contents to be written
            zf.close()

            # Grab ZIP file from in-memory, make response with correct MIME-type
            resp = HttpResponse(s.getvalue())
            # ..and correct content-disposition
            resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename

            return resp

        return super(FileList, self).get(request, format)


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

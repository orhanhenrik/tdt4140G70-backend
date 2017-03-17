from django.http import Http404
from django.urls import reverse
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import ListView
from django.http import HttpResponse
from files.models import File, Comment
from django.forms.models import modelform_factory
from django import forms

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

            checked_files = File.objects.filter(id__in=self.checked_files_ids).all()

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
                # Add file, at correct path
                zf.write(fpath, zip_path)

            # Must close zip for all contents to be written
            zf.close()

            # Grab ZIP file from in-memory, make response
            resp = HttpResponse(s.getvalue())
            # ..and correct content-disposition
            resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename

            return resp

        return super(FileList, self).get(request, format)


class FileUpload(CreateView):
    model = File
    template_name = 'files/upload.html'
    success_url = reverse_lazy('file-list')

    form_class = modelform_factory(File, fields=['file', 'course'],
                                   widgets={'file': forms.ClearableFileInput(attrs={'multiple': True})})

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        uploaded_files = request.FILES.getlist('file')

        if form.is_valid():
            for tuple_file in uploaded_files:
                tuple_name = tuple_file.name
                tuple_course = request.POST.get('course')
                print(tuple_name)
                print(tuple_course)
                # TODO: write to DB
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class CommentView(CreateView):
    def get_context_data(self, **kwargs):
        context = super(CommentView, self).get_context_data(**kwargs)
        try:
            context['file'] = File.objects.get(pk=self.kwargs['pk'])
        except File.DoesNotExist:
            raise Http404('File not found')
        return context

    def form_valid(self, form):
        form.instance.file_id = self.kwargs['pk']
        return super(CommentView, self).form_valid(form)

    model = Comment
    fields = ['text']
    template_name = 'files/comment.html'
    def get_success_url(self):
        return reverse('comment', kwargs=self.kwargs)

from django.http import Http404
from django.urls import reverse
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import ListView

from files.models import File, Comment


class FileList(ListView):
    queryset = File.objects.all()
    template_name = 'files/list.html'

    def get_context_data(self, **kwargs):
        context = super(FileList, self).get_context_data(**kwargs)
        all_files = File.objects.all()
        all_types = set()
        for file in all_files:
            name = file.filename()
            type = name[(name.index('.')+1):]
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


class FileUpload(CreateView):
    model = File
    fields = ['file', 'name', 'course']
    template_name = 'files/upload.html'

    success_url = reverse_lazy('file-list')

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

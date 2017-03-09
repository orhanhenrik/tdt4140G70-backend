from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import CommentForm

# Create your views here.
from django.urls import reverse
from django.views.generic import CreateView
from django.views.generic import ListView

from files.models import File


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

    def get_success_url(self):
        return reverse('file-list')

class CreateComment(CreateView):
    model = CreateComment
    fields = ['author', 'text']
    #template_name = 'files/add-comment'
    #render(request, 'files/add_comment_to_file.html', {'form': form})

"""
# Utgangspunkt
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'files/add_comment_to_file.html', {'form': form})
"""
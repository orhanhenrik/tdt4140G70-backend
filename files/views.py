from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from files.forms import DocumentForm
from files.models import File


def list(request):
    files = File.objects.all()
    return render(
        request,
        'files/list.html',
        {'files': files}
    )

def upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            file = File(file=request.FILES['file'], course_id=request.POST['course_id'])
            file.save()
        return HttpResponseRedirect(reverse('list-files'))
    else:
        form = DocumentForm()

    return render(
        request,
        'files/upload.html',
        {'form': form}
    )
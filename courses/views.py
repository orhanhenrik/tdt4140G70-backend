from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView

<<<<<<< HEAD
def get_courses(request):
    return render(request, 'courses/list_courses.html', {
        'message': "hi!",
    })
=======
from courses.models import Course


class Courses(ListView):
    queryset = Course.objects.all()
    template_name = 'courses/list.html'

class ViewCourse(DetailView):
    queryset = Course.objects.all()
    template_name = 'courses/detail.html'

class CreateCourse(CreateView):
    model = Course
    fields = ['name', 'description']
    template_name = 'courses/new.html'
    def get_success_url(self):
        return reverse('course-detail', args=(self.object.id,))

class UpdateCourse(UpdateView):
    model = Course
    fields = ['name', 'description']
    template_name = 'courses/edit.html'
    def get_success_url(self):
        return reverse('course-detail', args=(self.object.id,))
>>>>>>> f6927449efce2520868014555fe8916357e77bb2

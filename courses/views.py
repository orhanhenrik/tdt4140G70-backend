# Create your views here.
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView

from courses.models import Course


class Courses(ListView):
    queryset = Course.objects.all()
    template_name = 'courses/list.html'

class ViewCourse(LoginRequiredMixin, DetailView):
    queryset = Course.objects.all()
    template_name = 'courses/detail.html'

class CreateCourse(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = 'course.can_create'
    model = Course
    fields = ['name', 'description']
    template_name = 'courses/new.html'
    def get_success_url(self):
        return reverse('course-detail', args=(self.object.id,))

class UpdateCourse(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = 'course.can_update'
    model = Course
    fields = ['name', 'description']
    template_name = 'courses/edit.html'
    def get_success_url(self):
        return reverse('course-detail', args=(self.object.id,))


# Create your views here.
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from courses.models import Course


class Courses(ListView):
    queryset = Course.objects.all()
    template_name = 'courses/list.html'

class ViewCourse(LoginRequiredMixin, DetailView):
    queryset = Course.objects.all()
    template_name = 'courses/detail.html'

class CreateCourse(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = 'courses.add_course'
    model = Course
    fields = ['name', 'description']
    template_name = 'courses/new.html'
    def get_success_url(self):
        return reverse('course-detail', args=(self.object.id,))

class UpdateCourse(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = 'courses.change_course'
    model = Course
    fields = ['name', 'description']
    template_name = 'courses/edit.html'
    def get_success_url(self):
        return reverse('course-detail', args=(self.object.id,))

class DeleteCourse(PermissionRequiredMixin, DeleteView):
    permission_required = 'courses.delete_course'
    model = Course
    raise_exception = True
    success_url = reverse_lazy('course-list')

@login_required()
def subscribe_courses(request):
    action = request.POST.get('action')
    subscribe = True
    if action.startswith('subscribe'):
        course_ids = [action.replace('subscribe-','')]
    elif action.startswith('unsubscribe'):
        subscribe = False
        course_ids = [action.replace('unsubscribe-', '')]
    else:
        course_ids = request.POST.getlist('checks')
        if 'unsubscribe' in action:
            subscribe = False


    course_ids = list(map(int,course_ids))
    if subscribe:
        request.user.courses_subscribed_to.add(*course_ids)
    else:
        request.user.courses_subscribed_to.remove(*course_ids)
    return HttpResponseRedirect(reverse('course-list'))

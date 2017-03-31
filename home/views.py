from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import ListView
from django.http import HttpResponse
from django.http import HttpResponseRedirect

from courses.models import Course
from files.models import File
from django.db import models

@login_required()
def feed(request):
    user = get_user(request)
    print(user.courses_subscribed_to.all())
    courses = Course.objects.all()
    #courses = user.courses_subscribed_to.all()
    files = File.objects.all()
    return render(request, 'home/feed.html', {
        'courses': courses,
        'files': files
    })
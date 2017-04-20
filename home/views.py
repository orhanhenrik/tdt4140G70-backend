from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from files.models import File


@login_required()
def feed(request):
    courses = request.user.courses_subscribed_to.all()
    return render(request, 'home/feed.html', {
        'courses': courses
    })

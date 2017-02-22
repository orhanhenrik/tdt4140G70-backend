from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def get_courses(request):
    return render(request, 'courses/list_courses.html', {
        'message': "hi!",
    })
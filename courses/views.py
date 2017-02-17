from django.shortcuts import render

# Create your views here.


def get_courses(request):
    return render(request, 'courses/list_courses.html', {
        'message': "hi!",
    })
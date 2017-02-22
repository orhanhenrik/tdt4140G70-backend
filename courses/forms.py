from django.forms import ModelForm

from courses.models import Course


class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'description']
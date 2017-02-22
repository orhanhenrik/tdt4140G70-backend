from django.db import models

# Create your models here.
class File(models.Model):
    name = models.CharField(max_length=100, null=False)
    file = models.FileField(upload_to='files/')
    course = models.ForeignKey('courses.Course', related_name='files')

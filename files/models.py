from django.db import models
import os

# Create your models here.
class File(models.Model):
    name = models.CharField(max_length=100, null=False)
    file = models.FileField(upload_to='files/', null=False)
    course = models.ForeignKey('courses.Course', related_name='files')

    def filename(self):
        return os.path.basename(self.file.name)


from django.db import models

# Create your models here.
class Course(models.Model):
    name = models.CharField(max_length=50, null=False)
    description = models.TextField(null=False)


    def __str__(self):
        return self.name
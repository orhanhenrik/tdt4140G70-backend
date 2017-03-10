import base64
import json

import requests
from django.conf import settings
from django.db import models
import os

# Create your models here.
from django.utils.timezone import now
from django.db.models.signals import post_save
from django.dispatch import receiver


class File(models.Model):
    name = models.CharField(max_length=100, null=False)
    file = models.FileField(upload_to='files/', null=False)
    course = models.ForeignKey('courses.Course', related_name='files')

    def filename(self):
        return os.path.basename(self.file.name)

class Comment(models.Model):
    file = models.ForeignKey('files.File', related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(default=now, null=False)

    def __str__(self):
        return self.text

@receiver(post_save, sender=File)
def post_save_file(sender, instance, **kwargs):
    print(instance, kwargs)
    data = instance.file.read()
    b64_string = base64.b64encode(data)
    r = requests.post(
        '{}my_index/my_type/{}?pipeline=attachment'.format(settings.ES_URL, instance.id),
        data=json.dumps({
            "filename": str(instance.file),
            "data": b64_string.decode('utf-8')
        })
    )
    print(r)
    print(r.text)
    print(r.status_code)

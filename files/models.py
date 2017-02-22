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

from search.elasticsearch import elasticsearch


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


class FileDownloadLog(models.Model):
    file = models.ForeignKey('files.File', related_name = 'downloads')
    timestamp = models.DateTimeField(default = now, null = False)

    
@receiver(post_save, sender=File)
def post_save_file(sender, instance, **kwargs):
    print(instance, kwargs)
    data = instance.file.read()
    elasticsearch.add_to_index(instance.id, str(instance.file), data)

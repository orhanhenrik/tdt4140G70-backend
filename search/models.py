from django.db import models

# Create your models here.
from django.utils.timezone import now


class SearchLog(models.Model):
    search_term = models.CharField(max_length=200, null=False, db_index=True)
    timestamp = models.DateTimeField(default=now, null=False)

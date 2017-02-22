from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.list, name='list-files'),
    url(r'^upload$', views.upload, name='upload'),
]
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.list, name='file-list'),
    url(r'^upload$', views.upload, name='file-upload'),
]
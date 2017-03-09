from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.FileList.as_view(), name='file-list'),
    url(r'^upload$', views.FileUpload.as_view(), name='file-upload'),
    url(r'^add-comment$', views.CreateComment.as_view(), name='add-comment'),
]
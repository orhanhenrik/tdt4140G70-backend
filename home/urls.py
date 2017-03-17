from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.FeedView.as_view(), name='feed'),
]
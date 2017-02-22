from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.get_courses, name='index'),
    url(r'^$', views.index, name='index'),
    url(r'^tdt4140/', views.index, name = 'test'),
    url(r'^ttm4100/', views.index, name = 'test'),
    url(r'^tma4165/', views.index, name = 'test'),
    url(r'^tfe4105/', views.index, name = 'test')
]
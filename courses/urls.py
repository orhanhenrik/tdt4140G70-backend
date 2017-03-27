from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.Courses.as_view(), name='course-list'),
    url(r'^create', views.CreateCourse.as_view(), name='course-create'),
    url(r'^(?P<pk>[0-9]+)$', views.ViewCourse.as_view(), name='course-detail'),
    url(r'^(?P<pk>[0-9]+)/edit', views.UpdateCourse.as_view(), name='course-edit'),
    url(r'^(?P<pk>[0-9]+)/delete', views.DeleteCourse.as_view(), name='course-delete'),
]
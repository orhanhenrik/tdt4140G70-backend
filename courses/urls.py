from django.conf.urls import url

from . import views

urlpatterns = [
<<<<<<< HEAD
    url(r'^$', views.get_courses, name='index')
=======
    url(r'^$', views.Courses.as_view(), name='course-list'),
    url(r'^create', views.CreateCourse.as_view(), name='course-create'),
    url(r'^(?P<pk>[0-9]+)$', views.ViewCourse.as_view(), name='course-detail'),
    url(r'^(?P<pk>[0-9]+)/edit', views.UpdateCourse.as_view(), name='course-edit'),
>>>>>>> f6927449efce2520868014555fe8916357e77bb2
]
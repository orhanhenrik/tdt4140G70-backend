from django.test import TestCase
from django.urls import resolve
from django.urls import reverse

from courses.models import Course
from courses.views import Courses


class CourseTestCase(TestCase):
    fixtures = ['test_courses.json']

    def test_course_list(self):
        url = reverse('course-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertListEqual(list(response.context['object_list']), list(Course.objects.all()))


    def test_course_detail(self):
        course = Course.objects.first()
        url = reverse('course-detail', args=(course.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['object'], course)

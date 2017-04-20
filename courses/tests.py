from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve
from django.urls import reverse

from courses.models import Course
from courses.views import Courses


class CourseTestCase(TestCase):
    fixtures = ['test_users.yaml', 'test_courses.yaml']

    def test_str(self):
        course = Course.objects.first()
        self.assertEqual(str(course), course.name)

    def test_course_list(self):
        url = reverse('course-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertListEqual(list(response.context['object_list']), list(Course.objects.all()))


    def test_course_detail_without_auth(self):
        course = Course.objects.first()
        url = reverse('course-detail', args=(course.id,))
        response = self.client.get(url)
        self.assertRedirects(response, f'{reverse("account_login")}?next={url}')

    def test_course_detail(self):
        self.client.force_login(User.objects.first())
        course = Course.objects.first()
        url = reverse('course-detail', args=(course.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['object'], course)

    def test_subscribe_without_auth(self):
        url = reverse('course-subscribe')
        response = self.client.get(url)
        self.assertRedirects(response, f'{reverse("account_login")}?next={url}')

    def test_subscribe_courses(self):
        user = User.objects.first()
        user.courses_subscribed_to.clear()
        user.save()
        self.client.force_login(user)
        url = reverse('course-subscribe')
        response = self.client.post(url, {
            'action': 'subscribe-1'
        })
        self.assertRedirects(response, reverse('course-list'))
        self.assertListEqual(
            list(user.courses_subscribed_to.all()),
            [Course.objects.get(pk=1)]
        )
        response = self.client.post(url, {
            'action': 'unsubscribe-1'
        })
        self.assertRedirects(response, reverse('course-list'))
        self.assertListEqual(
            list(user.courses_subscribed_to.all()),
            []
        )

        response = self.client.post(url, {
            'action': 'multi-subscribe',
            'checks': [1, 2]
        })
        self.assertRedirects(response, reverse('course-list'))
        self.assertListEqual(
            list(user.courses_subscribed_to.all()),
            [Course.objects.get(pk=1), Course.objects.get(pk=2)]
        )

        response = self.client.post(url, {
            'action': 'subscribe-1',
        })
        self.assertRedirects(response, reverse('course-list'))
        self.assertListEqual(
            list(user.courses_subscribed_to.all()),
            [Course.objects.get(pk=1), Course.objects.get(pk=2)]
        )

        response = self.client.post(url, {
            'action': 'multi-unsubscribe',
            'checks': [2, 3]
        })
        self.assertRedirects(response, reverse('course-list'))
        self.assertListEqual(
            list(user.courses_subscribed_to.all()),
            [Course.objects.get(pk=1)]
        )

        response = self.client.post(url, {
            'action': 'multi-unsubscribe',
            'checks': [1]
        })
        self.assertRedirects(response, reverse('course-list'))
        self.assertListEqual(
            list(user.courses_subscribed_to.all()),
            []
        )

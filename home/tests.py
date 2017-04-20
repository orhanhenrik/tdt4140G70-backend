from django.contrib.auth.models import User
from django.test import TestCase

# Create your tests here.
from django.urls import reverse

from courses.models import Course


class FeedTestCase(TestCase):
    fixtures = ['test_users.yaml', 'test_courses.yaml']

    def test_without_auth(self):
        url = reverse('feed')
        response = self.client.get(url)
        self.assertRedirects(response, f'{reverse("account_login")}?next={url}')

    def test_without_subscriptions(self):
        user = User.objects.first()
        self.client.force_login(user)
        user.courses_subscribed_to.clear()
        url = reverse('feed')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertListEqual(
            list(response.context['courses']),
            []
        )

    def test_with_subscriptions(self):
        user = User.objects.first()
        self.client.force_login(user)
        user.courses_subscribed_to.clear()
        course = Course.objects.first()
        user.courses_subscribed_to.add(course)
        url = reverse('feed')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertListEqual(
            list(response.context['courses']),
            [course]
        )
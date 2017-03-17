from unittest import mock

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils.http import urlquote
from django.core.files.uploadedfile import SimpleUploadedFile

from courses.models import Course
from files.models import File


class CourseTestCase(TestCase):
    fixtures = ['test_users.yaml', 'test_courses.yaml']

    def test_search_without_auth(self):
        url = reverse('search')
        response = self.client.get(url)
        self.assertRedirects(response, f'{reverse("account_login")}?next={urlquote(url)}')

        url = f'{reverse("search")}?query=hello'
        response = self.client.get(url)
        self.assertRedirects(response, f'{reverse("account_login")}?next={urlquote(url)}')

    def test_search_get(self):
        self.client.force_login(User.objects.first())
        url = reverse('search')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.context['error'])
        self.assertEqual(len(response.context['results']), 0)

    @mock.patch('search.elasticsearch.Elasticsearch.search')
    @mock.patch('search.elasticsearch.Elasticsearch.add_to_index')
    def test_search_perform(self, add_to_index_mock, search_mock):
        filedata = b'hello world'
        file_object = SimpleUploadedFile('test.png', filedata)
        file = File.objects.create(
            name='test',
            course=Course.objects.first(),
            file=file_object
        )
        add_to_index_mock.assert_called_once_with(file.id, str(file.file), filedata)

        highlights = ['hello', 'world']

        search_mock.return_value = {
            'took': 100,
            'hits': {
                'hits': [
                    {
                        '_id': file.id,
                        'highlight': {
                            'attachment.content': highlights
                        }
                    }
                ]
            }
        }
        query = 'hello'
        self.client.force_login(User.objects.first())
        url = f'{reverse("search")}?query={query}'
        response = self.client.get(url)

        search_mock.assert_called_once_with(query)

        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.context['error'])
        self.assertEqual(len(response.context['results']), 1)
        self.assertEqual(response.context['results'][0][0], file)
        self.assertListEqual(response.context['results'][0][1], highlights)

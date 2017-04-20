import os
from io import BytesIO
from zipfile import ZipFile

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

# Create your tests here.
from django.urls import reverse

from courses.models import Course
from files.models import File


class FileTestCase(TestCase):
    fixtures = ['test_users.yaml', 'test_courses.yaml']

    def setUp(self):
        self.filedata = b'hello world'
        file_object = SimpleUploadedFile('test.txt', self.filedata)
        self.file = File.objects.create(
            name='test.txt',
            course=Course.objects.get(pk=1),
            file=file_object
        )
        self.filedata2 = b'hello world'
        file_object2 = SimpleUploadedFile('test.pdf', self.filedata2)
        self.file2 = File.objects.create(
            name='test.pdf',
            course=Course.objects.get(pk=1),
            file=file_object2
        )
        self.filedata3 = b'hello world'
        file_object3 = SimpleUploadedFile('test2.pdf', self.filedata3)
        self.file3 = File.objects.create(
            name='test2.pdf',
            course=Course.objects.get(pk=2),
            file=file_object3
        )

    def test_model(self):
        self.assertRegex(self.file.filename(), r'test_.+\.txt')
        self.assertEqual(self.file.extension(), 'txt')
        self.assertEqual(str(self.file), self.file.name)

    def test_comment_view(self):
        self.client.force_login(User.objects.first())
        url = reverse('comment', args=(self.file.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['file'], self.file)

    def test_comment_view_with_invalid_file_id(self):
        self.client.force_login(User.objects.first())
        url = reverse('comment', args=(100000,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_comment_view_without_auth(self):
        url = reverse('comment', args=(self.file.id,))
        response = self.client.get(url)
        self.assertRedirects(response, f'{reverse("account_login")}?next={url}')

    def test_comment_without_auth(self):
        url = reverse('comment', args=(self.file.id,))
        response = self.client.post(url)
        self.assertRedirects(response, f'{reverse("account_login")}?next={url}')

    def test_valid_comment(self):
        user = User.objects.first()
        self.client.force_login(user)

        url = reverse('comment', args=(self.file.id,))
        old_comments = set(self.file.comments.all())
        comment_text = 'hello'
        response = self.client.post(url, data={'text': comment_text})
        self.assertRedirects(response, url)
        new_comments = set(self.file.comments.all())
        self.assertEqual(len(new_comments) - len(old_comments), 1)
        comment = (new_comments - old_comments).pop()
        self.assertEqual(comment.created_by, user)
        self.assertEqual(comment.text, comment_text)
        self.assertEqual(comment.file, self.file)

    def test_file_upload_without_auth(self):
        url = reverse('file-upload')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)

    def test_file_upload_without_perms(self):
        user = User.objects.first()
        self.client.force_login(user)
        url = reverse('file-upload')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)

    def test_file_upload(self):
        user = User.objects.first()
        user.is_superuser = True
        user.save()
        self.client.force_login(user)

        course = Course.objects.first()
        filename = 'test.png'
        filedata = b'hello'
        file_object = SimpleUploadedFile(filename, filedata)
        old_files = set(File.objects.all())

        url = reverse('file-upload')
        response = self.client.post(url, {'course': course.id, 'file': file_object})
        self.assertRedirects(response, reverse('file-list'))

        new_files = set(File.objects.all())
        diff = new_files - old_files
        self.assertEqual(len(diff), 1)
        new_file = diff.pop()
        self.assertEqual(new_file.course, course)
        self.assertEqual(new_file.name, filename)
        self.assertEqual(new_file.file.read(), filedata)

    def test_file_multi_upload(self):
        user = User.objects.first()
        user.is_superuser = True
        user.save()
        self.client.force_login(user)

        course = Course.objects.first()
        filename = 'test.png'
        filedata1 = b'hello1'
        filedata2 = b'hello2'
        file_object1 = SimpleUploadedFile(filename, filedata1)
        file_object2 = SimpleUploadedFile(filename, filedata2)
        old_files = set(File.objects.all())

        url = reverse('file-upload')
        response = self.client.post(url, {'course': course.id, 'file': [file_object1, file_object2]})
        self.assertRedirects(response, reverse('file-list'))

        new_files = set(File.objects.all())
        diff = new_files - old_files
        self.assertEqual(len(diff), 2)
        new_file1 = diff.pop()
        new_file2 = diff.pop()

        self.assertEqual(new_file1.course, course)
        self.assertEqual(new_file2.course, course)
        self.assertEqual(new_file1.name, filename)
        self.assertEqual(new_file2.name, filename)

        self.assertListEqual(
            [new_file1.file.read(), new_file2.file.read()],
            [filedata1, filedata2]
        )

    def test_file_list_types(self):
        user = User.objects.first()
        self.client.force_login(user)
        url = reverse('file-list')
        response = self.client.get(url)
        self.assertSetEqual(
            response.context['file_types_list'],
            {'pdf', 'txt'}
        )

    def test_only_list_files_for_subscribed_course(self):
        user = User.objects.first()
        self.client.force_login(user)

        url = reverse('file-list')
        response = self.client.get(url)
        self.assertListEqual(
            list(response.context['files']),
            []
        )

        course = Course.objects.get(pk=2)
        user.courses_subscribed_to.add(course)
        response = self.client.get(url)
        self.assertListEqual(
            list(response.context['files']),
            [self.file3]
        )

    def test_list_filter_by_filetype(self):
        user = User.objects.first()
        user.courses_subscribed_to.add(*Course.objects.all())

        self.client.force_login(user)

        url = '{}?filetype_choice=txt'.format(reverse('file-list'))
        response = self.client.get(url)
        self.assertListEqual(
            list(response.context['files']),
            [self.file]
        )

        url = '{}?filetype_choice=pdf'.format(reverse('file-list'))
        response = self.client.get(url)
        self.assertListEqual(
            list(response.context['files']),
            [self.file3, self.file2]
        )


    def test_multi_download(self):
        user = User.objects.first()
        self.client.force_login(user)
        url = '{}?checks={}&checks={}'.format(reverse('file-list'), self.file2.id, self.file3.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Disposition'], 'attachment; filename=crawlingfiles.zip')
        s = BytesIO()
        s.write(response.content)
        zip = ZipFile(s)
        files = {os.path.basename(n): zip.read(n) for n in zip.namelist()}
        self.assertIn(self.file2.filename(), files)
        self.assertIn(self.file3.filename(), files)
        self.assertEqual(files[self.file2.filename()], self.filedata2)
        self.assertEqual(files[self.file3.filename()], self.filedata3)


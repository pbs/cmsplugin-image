from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from django.conf import settings
from filer.models import File, Image
import json
import os


class TestFile(TestCase):

    def setUp(self):
        username, password = 'mock_user_%$#!_1234', 'mock'
        User.objects.create_superuser(
            username=username,
            password=password,
            email=username + '@test.com'
        )
        self.client.login(username=username, password=password)

    def _get_file_data(self, filename):
        return {
            'original_filename': filename,
            'file': SimpleUploadedFile(filename, 'these are the file contents!')
        }

    def assertContent(self,  _file, _expected_result, file_type=None):
        response = self.client.get(
            '/imagefield/get_file/',
            {'id':_file.id, 'file_type': file_type or ''},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        url = json.loads(response.content).get('url', '')
        self.assertEqual(url, _expected_result)

    def test_file(self):
        filer_file = File.objects.create(**self._get_file_data('file.txt'))
        self.assertContent(filer_file, '')
        self.assertContent(filer_file, filer_file.file.url, file_type='file')

    def test_image(self):
        filer_image = Image.objects.create(**self._get_file_data('file.png'))
        self.assertContent(filer_image, filer_image.file.url)
        self.assertContent(filer_image, '', file_type='file')

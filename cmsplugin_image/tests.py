import unittest
from django.test.client import Client
from filer.models import File, Folder
import ast
from django.contrib.auth.models import User

class TestFile(unittest.TestCase):

    fixtures = ['mock_data.json' ]

    def setUp(self):
        self.client = Client()
        self.logged_in = False
        self.mock_user = None
        try:
            user = User.objects.get(username__exact='mock_user_%$#!_1234')
        except User.DoesNotExist:
            user = None
        if not user:
            self.mock_user = User.objects.create_superuser(username='mock_user_%$#!_1234', password='mock', email='mock@mock.com')
        if not self.logged_in:
            self.logged_in = self.client.login(username='mock_user_%$#!_1234', password='mock')

    def tearDown(self):
        if self.mock_user:
            self.mock_user.delete()

    def assertContent(self,  _file, _expected_result):
        if not self.logged_in:
            self.fail("Could not login to the admin interface.")
        else:
            response = self.client.get('/imagefield/get_file/', {'id':_file.id}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
            content_dict = ast.literal_eval(response.content)
            self.assertEqual(content_dict.get('url', ''), _expected_result)

    def test_txt(self):
        file = File.objects.get(pk=1)
        self.assertContent(file, '')
        self.tearDown()

    def test_png(self):
        file = File.objects.get(pk=2)
        self.assertContent(file, file.file.url)
        self.tearDown()

    def test_jpeg(self):
        file = File.objects.get(pk=3)
        self.assertContent(file, file.file.url)
        self.tearDown()
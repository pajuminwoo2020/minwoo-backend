from django.test import TestCase
from django.urls import reverse

from user.models import User


class UserCreateTest(TestCase):
    databases = '__all__'
    test_userid = 'chan@tvengers.com'
    test_password = '1234abc1'
    test_fullname = 'tvengers'

    def setUp(self):
        password = 'chan'

    def test_user_create_should_succeed(self):
        response = self.client.post(reverse('user:user_create'), data={
            'userid': self.test_userid,
            'fullname_local': self.test_fullname,
            'password': self.test_password
        }, content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('userid', None), self.test_userid)
        self.assertEqual(response.json().get('fullname', None), self.test_fullname)

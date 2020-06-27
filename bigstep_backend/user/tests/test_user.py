from django.test import TestCase

from user.models import User


class UserCreateTest(TestCase):
    databases = '__all__'
    test_fullname = 'tvengers'
    test_password = '12341234'

    def setUp(self):
        email = 'chan@tvengers.com'
        password = 'chan'
        user = User.objects.create_user(userid=email, password=password, fullname='Chan', is_active=True)

    def test_user_create_should_succeed(self):
        pass

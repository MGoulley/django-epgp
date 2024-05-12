from django.test import TestCase
from django.contrib.auth.models import User

# Create your tests here.

class UserTestCase(TestCase):
    
    def setUp(self):
        User.objects.create_user(username='oscaro.com', password='password', email='oscar.blkd@gmail.com')
    
    def test_user_get(self):
        self.assertEqual(User.objects.get(email='oscar.blkd@gmail.com'), User.objects.get(username='oscaro.com'))
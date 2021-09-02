from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse


# Create your tests here.
class UserTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            full_name='zahra',
            email='zahra.kh2005@email.com',
            password='123456'
        )
        self.assertEqual(user.full_name, 'zahra')
        self.assertEqual(user.email, 'zahra.kh2005@email.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staffs)
        self.assertFalse(user.is_admin)

    def test_create_superuser(self):
        User = get_user_model()

        admin_user = User.objects.create_superuser(
            full_name='zahra_admin',
            email='zahra_admin@email.com',
            password='123456'
        )
        self.assertEqual(admin_user.full_name, 'zahra_admin')
        self.assertEqual(admin_user.email, 'zahra_admin@email.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staffs)
        self.assertTrue(admin_user.is_admin)


class SignupTests(TestCase):
    full_name = 'zahra_user'
    email = 'zahra_user@email.com'

    def setUp(self):
        url = reverse('accounts:register')
        self.response = self.client.get(url)

    def test_signup_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'accounts/register.html')
        self.assertContains(self.response, 'Register')  # value="Register" button for register.html page
        self.assertNotContains(
            self.response, 'not be on the page.')


class LogInTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.credentials = {
            'email': 'testuser@gmail.com',
            'full_name': 'testuser',
            'password': '123456'}
        User.objects.create_user(**self.credentials)

    def test_login(self):
        # send login data
        response = self.client.post('/login/', self.credentials, follow=True)
        # should be logged in now
        # self.assertTrue(response.context['user'].is_active)

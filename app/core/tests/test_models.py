from django.test import TestCase
from django.contrib.auth import get_user_model

class ModelTests(TestCase):

    def test_create_user_with_email_success(self):
        """ Test to check if our user is created successfully or not"""

        email='vedant.jolly@spit.ac.in'
        password='BassCoder2808'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email,email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """To test the email for a new user is normalized or not"""

        email = "vedantjolly2001@gmail.com"
        user = get_user_model().objects.create_user(email,'BassCoder2808')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """To test that creating a user without an email raises an error"""

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None,'123')

    def test_create_new_superuser(self):
        """To test that we can create a superuser or not"""

        user = get_user_model().objects.create_superuser('vedantjolly2001@gmail.com','12345')

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
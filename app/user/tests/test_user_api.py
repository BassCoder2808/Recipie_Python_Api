from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """To test ou User API's"""

    def setup(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test to check if a user is created with a valid payload"""
        payload = {
            'email': 'vedant.jolly@spit.ac.in',
            'password': 'BassCoder2808',
            'name': 'Vedant Jolly',
        }

        res = self.client.post(CREATE_USER_URL, payload)
        user = get_user_model().objects.get(**res.data)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """Test that should fail if a user already exists"""
        payload = {
            'email': 'vedant.jolly@spit.ac.in',
            'password': 'BassCoder2808',
            'name': 'Test',
        }

        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that should fail when a user enters a short password"""
        payload = {
            'email': 'vedant.jolly@spit.ac.in',
            'password': 'Bass',
            'name': 'Test',
        }

        res = self.client.post(CREATE_USER_URL, payload)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test if a token is generated for a new user"""
        payload = {
            'email': 'vedantjolly2001@gmail.com',
            'password': 'BassCoder2808'
        }
        create_user(**payload)

        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test to check if a token is created for invalid credentials"""
        create_user(email='vedantjolly2001@gmail.com', password='BassCoder2808')

        payload = {
            'email': 'vedantjolly2001@gmail.com',
            'password': 'basscoder2808',
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Token should not be created when a user doesn't exists"""
        payload = {
            'email': 'vedantjolly2001@gmail.com',
            'password': 'basscoder2808',
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_fields(self):
        """Token should not be created when the fields are missing"""
        payload = {
            'email': 'vedantjolly2001@gmail.com',
            'password': '',
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    # def test_retrieve_user_unauthorized(self):
    #     """Test that authentication is required for the users"""
    #
    #     res = self.client.get(ME_URL)
    #
    #     self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """Tests that require user authentication"""

    def setUp(self):
        self.user = create_user(
            email='vedant@gmail.com',
            password='BassCoder2808',
            name='password'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieving profile for the logged in user"""

        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.email,
        })

    def test_me_post_not_allowed(self):
        """Post method is not allowed"""

        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test for updating the user"""

        payload = {
            'name': 'basscoder2808',
            'password': 'VeduVediJJ'
        }

        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()

        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

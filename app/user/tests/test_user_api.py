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
    """Test the users api (public)"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test if user is created successfully"""

        payload = {
            'email': 'test@testuser.com',
            'password': 'supersecretpassword',
            'name': 'Test User'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        # GET object from the database to make sure it was created
        # properly, by passing in the response data from the API.
        user = get_user_model().objects.get(**res.data)
        # Check password by using the built-in Django function
        self.assertTrue(user.check_password(payload['password']))
        # make sure the password, even the encrypted one, is not
        # returned to the user as a security precaution.
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """Test if creating a user already exists"""

        payload = {
            'email': 'test@testuser.com',
            'password': 'supersecretpassword',
            'name': 'Test User'
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        # The response we expect if a create user request is sent for
        # a user that already exists.
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that password is more than 5 characters"""
        payload = {
            'email': 'test@testuser.com',
            'password': 'pw',  # i.e., bad password
            'name': 'Test User'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test that a token was created for a user"""
        payload = {'email': 'test@test.com', 'password': 'testpass'}
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # NOTE: there's no need to test whether or not the user is
        # authenticated since, presumably, Django developers already did

    def test_create_token_invalid_credentials(self):
        """Test that user provides valid credentials when creating token"""
        create_user(email='test@test.com', password='testpass')
        payload = {'email': 'test@test.com', 'password': 'wrongpass'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test that token is not created when user does not exist"""
        payload = {'email': 'test@test.com', 'password': 'testpass'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Test that token is not created if a field is blank"""
        res = self.client.post(TOKEN_URL, {'email': 'one', 'password': ''})

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """Test that authentication is required to access a user"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """Test API requests that require authentication"""

    def setUp(self):
        self.user = create_user(
            email='test@test.com',
            password='testpass',
            name='name'
        )
        # set up the client
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged in user"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.email
        })

    def test_post_me_not_allowed(self):
        """Test that post requests are forbidden on ME_URL"""
        res = self.client.post(ME_URL, {})  # send post request with no data

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating user profile for authenticated user"""
        payload = {'name': 'newname', 'password': 'newpassword'}

        res = self.client.patch(ME_URL, payload)

        # get latest data from db from user model object
        self.user.refresh_from_db()
        # check that the new name/password was applied
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        # for good measure, check that the request returns a 200
        self.assertEqual(res.status_code, status.HTTP_200_OK)

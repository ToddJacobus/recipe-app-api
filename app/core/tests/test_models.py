from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test whether creating a user with an email is successful"""
        email = "ilike@pples.yum"
        password = "banana"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password, password)

    def test_new_user_email_is_normalized(self):
        """Test wether a new user email is normalized, i.e., all lower case."""
        email = "thisisreally@BANANAS.COM"
        user = get_user_model().objects.create_user(email, "secret123")

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test whether user email is invalid"""
        with self.assertRaises(ValueError):
            # everything in this context manager should raise
            # a value error (i.e., assert that ValueError will
            # be raised)
            # In the case below, test whether or not the email field as None
            # will raise a ValueError, which it should.
            user = get_user_model().objects.create_user(None, "sectret123")

    def test_create_new_superuser(self):
        """Can we create a new superuser?"""
        user = get_user_model().objects.create_superuser(
            email="superb@na.na",
            password="ihaveallthepower"
        )
        # is_superuser attribute comes from PermissionsMixin
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff) # attribute of user from model
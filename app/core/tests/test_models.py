from unittest.mock import patch

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def sample_user(email='test@email.com', password='testpass'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


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
            get_user_model().objects.create_user(None, "sectret123")

    def test_create_new_superuser(self):
        """Can we create a new superuser?"""
        user = get_user_model().objects.create_superuser(
            email="superb@na.na",
            password="ihaveallthepower"
        )
        # is_superuser attribute comes from PermissionsMixin
        self.assertTrue(user.is_superuser)
        # attribute of user from model
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """Test the tag string representation"""
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Vegan'
        )

        self.assertEqual(str(tag), tag.name)

    def test_ingredients_str(self):
        """Test the ingredient string representation"""
        ingredient = models.Ingredient.objects.create(
            user=sample_user(),
            name='Cucumber'
        )

        self.assertEqual(str(ingredient), ingredient.name)

    def test_recipe_str(self):
        """Test the recipe string representation"""
        recipe = models.Recipe.objects.create(
            user=sample_user(),
            title='steak and mushroom sauce',
            time_minutes=5,
            price=5.00
        )

        self.assertEqual(str(recipe), recipe.title)

    @patch('uuid.uuid4')
    def test_recipe_filename_uuid(self, mock_uuid):
        """test that image is saved in the correct location"""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.recipe_image_file_path(None, 'my_image.jpg')

        exp_path = f'uploads/recipe/{uuid}.jpg'
        self.assertEqual(file_path, exp_path)

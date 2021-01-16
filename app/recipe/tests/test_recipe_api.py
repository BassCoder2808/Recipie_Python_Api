from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe, Tag, Ingredient

from recipe.serializers import RecipeSerializer, RecipeDetailSerializer

RECIPIES_URL = reverse('recipe:recipe-list')


def detail_url(recipe_id):
    """Return a recipe detail url"""

    return reverse('recipe:recipe-detail', args=[recipe_id])


def sample_recipe(user, **params):
    """Creating and returning a sample recipe"""
    defaults = {
        'title': 'Sample Recipe',
        'time_minutes': 5,
        'price': 5.00
    }

    defaults.update(params)

    return Recipe.objects.create(user=user, **defaults)


def sample_tag(user, name='Main Course'):
    """Return a sample tag"""

    return Tag.objects.create(user=user, name=name)


def sample_ingredient(user, name='Kale'):
    """Return a sample ingredient"""

    return Ingredient.objects.create(user=user, name=name)


class PublicRecipeApiTest(TestCase):
    """Public Recipe APi test"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required"""

        res = self.client.get(RECIPIES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeApiTest(TestCase):
    """Private test which required a logged in user"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'vedant@gmail.com',
            'basscoder2808'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_recipies(self):
        """Test that retrieves all the recipies"""

        sample_recipe(user=self.user)
        sample_recipe(user=self.user)

        res = self.client.get(RECIPIES_URL)

        recipies = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipies, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_recipe_linited_to_user(self):
        """Test that a user can retrieve his recipies only"""

        user2 = get_user_model().objects.create_user(
            'jolly@gmail.com',
            'basscoder'
        )

        sample_recipe(user=self.user)
        sample_recipe(user=user2)

        res = self.client.get(RECIPIES_URL)

        recipies = Recipe.objects.filter(user=self.user).order_by('-id')
        serializer = RecipeSerializer(recipies, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)

    def test_recipe_detail(self):
        """Test the detail view ofn our Recipe API"""

        recipe = sample_recipe(user=self.user)
        recipe.tags.add(sample_tag(user=self.user))
        recipe.ingredients.add(sample_ingredient(user=self.user))

        url = detail_url(recipe.id)

        res = self.client.get(url)
        serializer = RecipeDetailSerializer(recipe)

        self.assertEqual(res.data, serializer.data)

    def test_create_basic_recipe(self):
        """Creating a basic recipe"""

        payload = {
            'title': 'Chocolate Cake',
            'time_minutes': 5,
            'price': 7.50
        }

        res = self.client.post(RECIPIES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        recipe = Recipe.objects.get(id=res.data['id'])

        for key in payload.keys():
            self.assertEqual(payload[key], getattr(recipe, key))

    def test_create_recipe_with_tags(self):
        """Creating a recipe with tags"""

        tag1 = sample_tag(user=self.user, name='Vegan')
        tag2 = sample_tag(user=self.user, name='Kale')

        payload = {
            'title': 'Chocolate Cake',
            'tags': [tag1.id, tag2.id],
            'time_minutes': 5,
            'price': 7.50
        }

        res = self.client.post(RECIPIES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        recipe = Recipe.objects.get(id=res.data['id'])
        tags = recipe.tags.all()

        self.assertEqual(tags.count(), 2)
        self.assertIn(tag1, tags)
        self.assertIn(tag2, tags)

    def test_create_recipe_with_ingredients(self):
        """Create a recipe with ingredients"""

        ingredient1 = sample_ingredient(user=self.user, name='Cocoa')
        ingredient2 = sample_ingredient(user=self.user, name='Beetel Leaf')

        payload = {
            'title': 'Chocolate Cake',
            'ingredients': [ingredient1.id, ingredient2.id],
            'time_minutes': 5,
            'price': 7.50
        }

        res = self.client.post(RECIPIES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        recipe = Recipe.objects.get(id=res.data['id'])
        ingredients = recipe.ingredients.all()

        self.assertEqual(ingredients.count(), 2)
        self.assertIn(ingredient1, ingredients)
        self.assertIn(ingredient2, ingredients)

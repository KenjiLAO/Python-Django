from django.test import TestCase
from django.utils.text import slugify
from blog.models import Categorie, Tag

class CategorieModelTest(TestCase):
    def test_get_absolute_url(self):
        categorie = Categorie.objects.create(nom="Plats Végétariens", slug=slugify("Plats Végétariens"))
        expected_url = f"/categories/{categorie.slug}/"
        self.assertEqual(categorie.get_absolute_url(), expected_url)


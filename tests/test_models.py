from django.test import TestCase
from purbeurre.models import Categories, Products


# models test
class CategoriesTestCase(TestCase):

    def create_categories(self, category_name="Biscuits"):
        return Categories.objects.create(category_name=category_name)

    def test_categories_creation(self):
        w = self.create_categories()
        self.assertTrue(isinstance(w, Categories))
        self.assertEqual("Biscuits", w.category_name)

    def test_model_str(self):
        w = self.create_categories()
        self.assertEqual(str(w.category_name), "Biscuits")


# models test
class ProductsTestCase(TestCase):

    def create_categories(self, categories_name="Pâtes à tartiner"):
        return Categories.objects.get_or_create(category_name=categories_name)

    def create_products(self):
        cat, created = self.create_categories()

        return Products.objects.create(id_product=1, product_name="nutella", url="http://", img="http://",
                                       nutrition_score="e", category=cat)

    def test_id_product(self):
        # test product id
        nutella = self.create_products()
        self.assertTrue(isinstance(nutella, Products))
        self.assertEqual(1, nutella.id_product)

    def test_product_name(self):
        # test product name
        nutella = self.create_products()
        self.assertEqual('nutella', nutella.product_name)
        self.assertIsInstance(nutella.product_name, str)

    def test_nutrition_score(self):
        # test nutrition score
        nutella = self.create_products()
        self.assertEqual('e', nutella.nutrition_score)

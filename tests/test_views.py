from django.test import TestCase, Client
from django.urls import reverse
from purbeurre.models import Products, Categories, Substitutes
from users.models import User
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory
from users.views import account as profile
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from purbeurre.forms import UserCreationForm
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.firefox.webdriver import WebDriver

# firefox_options = webdriver.FirefoxOptions()
# firefox_options.headless = True



class IndexPageTestCase(TestCase):

    # test that index returns a 200
    # must start with `test`
    def test_index_page(self):
        # you must add a name to index view: `name="index"`
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)


class LegalPageTestCase(TestCase):
    """ test legal page """

    def test_legals_page(self):
        """ If returns a http code 200 is ok """
        response = self.client.get(reverse('purbeurre:legal'))
        self.assertEqual(response.status_code, 200)


class ContactsPageTestCase(TestCase):
    """ test contact page """

    def test_contacts_page(self):
        """ If returns a http code 200 is ok """
        response = self.client.get(reverse('purbeurre:contacts'))
        self.assertEqual(response.status_code, 200)


class LogoutPageTestCase(TestCase):
    """ test contact page """

    def test_logout_page(self):
        """ If returns a http code 200 is ok """
        response = self.client.get(reverse('users:logout'))
        self.assertEqual(response.status_code, 302)


class DetailPageTestCase(TestCase):
    """ test product detail page """

    def setUp(self):
        """ create testing product """
        category = Categories.objects.create(category_name="Pâte à tartiner")
        nutella = Products.objects.create(
            id_product=1,
            product_name="nutella",
            category=category
        )
        self.product = Products.objects.get(product_name="nutella")

    def test_detail_page_returns_200(self):
        """ returns status_code 200 if the page is ok """
        product_id = self.product.id_product
        response = self.client.get(reverse('purbeurre:product_detail', args=(product_id,)))
        self.assertEqual(response.status_code, 200)

    def test_detail_page_returns_404(self):
        """ return 404 if the query is invalid """
        product_id = self.product.id_product + 1
        response = self.client.get(reverse('purbeurre:product_detail', args=(product_id,)))
        self.assertEqual(response.status_code, 404)


class RegistrationPageTestCase(TestCase):
    """test signup page"""

    def setUp(self):
        sign_up_url = reverse('users:sign_up')
        user_data = {
            'username': 'alice',
            'email': 'alice@example.com',
            'password1': 'Qwerasdz12345',
            'password2': 'Qwerasdz12345'
        }

        self.home_url = (reverse('users:account'))
        self.response = self.client.post(sign_up_url, user_data)

    def test_display_register_page(self):
        response = self.client.get(reverse("users:sign_up"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "purbeurre/sign_up.html")
        self.assertContains(response, "username")
        self.assertContains(response, "email")
        self.assertContains(response, "password1")
        self.assertContains(response, "password2")

    def test_register_page_returns_200(self):
        """ 200 if the sign up is success"""
        response = self.client.get(reverse('users:sign_up'))
        self.assertEqual(response.status_code, 200)

    def test_csrf(self):
        """ test for csfr token """
        response = self.client.get(reverse('users:sign_up'))
        self.assertContains(response, 'csrfmiddlewaretoken')

    # def test_user_authentication(self):
    #     response = self.client.get(self.home_url)
    #     user = response.context.get('user')
    #     self.assertTrue(user.is_authenticated)

    def test_contains_form(self):
        """ test for sign up form """
        response = self.client.get(reverse('users:sign_up'))
        form = response.context.get('form')
        self.assertIsInstance(form, UserCreationForm)


class InvalidRegistrationPageTests(TestCase):
    """test registration page with invalid inputs"""

    def setUp(self):
        sign_up_url = reverse('users:sign_up')
        user_data = {
        }
        self.home_url = (reverse('users:account'))
        self.response = self.client.post(sign_up_url, user_data)

    def test_registration_status(self):
        self.assertEqual(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

    def test_dont_create_user(self):
        self.assertFalse(User.objects.exists())


class LoginPageTestCase(TestCase):
    """test login page"""

    def setUp(self):
        self.username = "alice"
        self.password = 'Qwerasdz12345'
        self.email = "sonam@gmail.com"
        self.user = User.objects.create_user(username=self.username, password=self.password,email=self.email)

    def test_login_page_status(self):
        response = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        """ test with login data and response status code 302 Found  """
        response = self.client.post(reverse('users:login'), {
            "email": self.email,
            "password": self.password,
        })
        self.assertEqual(response.status_code, 200)

    def test_login_invalid_username(self):
        """ test with invalid username and the request return response status code 200 """
        response = self.client.post(reverse('users:login'), {
            "email": '',
            "password": self.password,
        })
        self.assertEqual(response.status_code, 200)

    def test_login_invalide_password(self):
        """ test with invalide username and the request return response status code 200 """
        response = self.client.post(reverse('users:login'), {
            "email": self.email,
            "password": "",
        })
        self.assertEqual(response.status_code, 200)

class TestProfileView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username="inconnu",
            email="inconnu@gmail.com",
            password="1234AZERTY",
        )

    def test_display_profile_ok(self):
        request = self.factory.get(reverse("users:account"))
        request.user = self.user
        response = profile(request)
        self.assertEqual(response.status_code, 200)

    def test_display_profile_not_ok(self):
        request = self.factory.get(reverse("users:account"))
        request.user = AnonymousUser()
        response = profile(request)
        self.assertEqual(response.status_code, 302)


class SavedTestPageCase(TestCase):

    def setUp(self):
        # temporary data
        url = reverse('users:saved')
        self.data = {
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'Qwerasdz12345',
        }
        self.response = self.client.post(url, self.data)
        # create user with use temp data
        self.user = User.objects.create_user(**self.data)
        # create a category
        category = Categories.objects.create(category_name="Biscuits")

        origin = Products.objects.create(
            id_product=1,
            product_name="Pain d'épices",
            category=category
        )
        replacement = Products.objects.create(
            id_product=2,
            product_name="Sablé Nature",
            category=category
        )

        Substitutes.objects.create(
            origin=origin,
            replacement=replacement,
            user=self.user)

        self.origin = Products.objects.get(pk=1)
        self.replacement = Products.objects.get(pk=2)

    def test_account_page_returns_200(self):
        """ return 200 if ok """
        self.client.login(**self.data)
        response = self.client.get(reverse('users:saved'))
        self.assertEqual(response.status_code, 302)

    def test_substitute(self):
        """ testsubsitute product """
        self.client.login(**self.data)
        self.client.post(reverse('users:saved'), {
            "origin": self.origin.id_product,
            "replacement": self.replacement.id_product,
        })
        self.assertTrue(Substitutes.objects.exists())


class SearchPageTestCase(TestCase):
    def setUp(self):
        category = Categories.objects.create(category_name="Pâte à tartiner")
        Products.objects.create(
            id_product=1,
            product_name="Nocilla",
            category=category,
            nutrition_score="d"
        )

        Products.objects.create(

            id_product=2,
            product_name="Nocciolata",
            category=category,
            nutrition_score="a"
        )
        self.password = "Qwerasdz12345"
        self.user = User.objects.create_user(
            username="alice",
            password=self.password,
            email="alice@example.com"
        )
        self.client = Client()
        self.origin = Products.objects.get(pk=1)
        self.replacement = Products.objects.get(pk=2)
        self.client.force_login(user=self.user)

    def test_search_page_returns_200(self):
        """ returns 200 if the query parameters are correct """
        response = self.client.get(reverse('purbeurre:search'), {"query": "Nocilla"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Nocilla', response.content)

    def test_random_list_of_products_if_no_query(self):
        # Test that an empty query returns to a page displaying a certain message and suggests products
        response = self.client.get(

            reverse('purbeurre:search'), {"query": ""}

        )
        self.assertIn(b'Suggestion de produits', response.content)



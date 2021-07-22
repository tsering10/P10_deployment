""" 
Script to populate and update PurBeurre database with
OpenFoodFactsdata API"""

# ----------------------------------------------------------------------------------------------------------
# To run this script run "manage.py db_loading" command in your console.
# ----------------------------------------------------------------------------------------------------------


# Imports
import requests
from django.core.management.base import BaseCommand
from purbeurre.models import Categories, Products
from django.db import IntegrityError


class Command(BaseCommand):
    """
    Class to handle the "manage.py db_loading" command.
    This class is used to update database with data from OpenFoodFacts.
    """

    help = "Use this script to update the database from OpenFoodFacts"

    def handle(self, *args, **kwargs):
        """
        Handle updating process
        """

        # Gives infos about updating process
        self.stdout.write("Updating PurBeurre database...", ending='\n')

        # selected categories (according to openfood facts documentation)
        categories = [
            "Biscuits et gâteaux",
            "Desserts",
            "Confitures",
            "Pizzas",
            "Pâtes à tartiner",
            "Céréales et pommes de terre",
            "Boissons",
            "Produits laitiers",
            "Produits à tartiner",
            "Petit-déjeuners",
            "Charcuteries",
            "Chocolats",
            "Poissons",
            "Jambons"
        ]

        # For each category
        for category in categories:
            # populate data into DB
            products = self._request_off_api(category)
            self._insert(products)

    def _request_off_api(self, category):

        '''
        This method is use to request the openfoodfacts api 
        and get the data of respective category
        '''
        # api url 
        api_url = "https://fr.openfoodfacts.org/cgi/search.pl"

        # parameters to be used for the requests method
        params = {
            'tagtype_0': 'categories',
            'tag_contains_0': 'contains',
            'tag_0': category,
            'action': 'process',
            'json': '1',
            'page_size': '250'
        }

        try:
            products_data = requests.get(api_url, params=params)
            products_data = products_data.json()
            data = []
            nutrition_score = ['a','b','c','d','e']
            for i, _ in enumerate(products_data["products"]):
                if "".join(products_data["products"][i]["nutrition_grades_tags"]) in nutrition_score:
                    try:
                        extract_data= {
                                        "product_name": products_data["products"][i].get('product_name'),
                                        "product_id": int(products_data["products"][i].get("_id")),
                                        "product_url": products_data["products"][i].get("url"),
                                        "product_img": products_data["products"][i].get("image_small_url"),
                                        "nutriscore": str(*products_data["products"][i].get("nutrition_grades_tags")),
                                        "fat":products_data["products"][i]["nutriments"].get("fat_100g"),
                                        "saturated_fat": products_data["products"][i]["nutriments"].get("saturated-fat_100g"),
                                        "salt": products_data["products"][i]["nutriments"].get("salt_100g"),
                                        "sugar": products_data["products"][i]["nutriments"].get("sugars_100g"),
                                        "categories": products_data["products"][i]["categories"].split(',')[:1]

                                    }
            
                        data.append(extract_data)
                    except KeyError:
                        pass
            return data
        except requests.exceptions.ConnectionError:
            print("You must be connected in order to create or update the database")


    def _insert(self, products_data):
        
        """
        This method is use to populate the database 
        """
        for prod in products_data:

            # fill Categories table with openfoodfacts data or create new ones if necessary
            try:
                cat, _ = Categories.objects.get_or_create(
                    category_name = prod["categories"]
                    )

                # fill products table with OpenFactsFood data or create new ones if necessary
                Products.objects.update_or_create(
                    id_product = prod["product_id"],
                    product_name = prod["product_name"],
                    url = prod["product_url"],
                    img = prod["product_img"],
                    nutrition_score = prod["nutriscore"],
                    fat = prod["fat"],
                    saturated_fat = prod["saturated_fat"],
                    salt = prod["salt"],
                    sugar = prod["sugar"],
                    category = cat
                )
            # Ignore duplicate value
            except IntegrityError:
                continue
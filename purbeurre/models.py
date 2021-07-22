from django.db import models
from users.models import User
# from django.contrib.auth.models import User


# Create your models here.

class Categories(models.Model):
    """Model for creating OpenFoodFacts categories"""
    category_name = models.CharField(max_length=500, unique=True)

    def __str__(self):
        return self.category_name


class Products(models.Model):
    """Model for creating OpenFoodFacts products"""
    id_product = models.BigIntegerField(primary_key=True)
    product_name = models.CharField(max_length=255)
    url = models.URLField()
    img = models.URLField()
    fat = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    saturated_fat = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    salt = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    sugar = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    nutrition_score = models.CharField(max_length=1, null=True)
    category = models.ForeignKey("Categories", on_delete=models.CASCADE)

    def __str__(self):
        return str({
            "id_product": self.id_product,
            "product_name": self.product_name,
            "url": self.url,
            "image": self.img,
            "nutrition_score": self.nutrition_score,
            "category": self.category
        })


class Substitutes(models.Model):
    """Table association between products and user to save a chosen substitute product for a specific user"""
    origin = models.ForeignKey(Products, related_name='origin', on_delete=models.CASCADE)
    replacement = models.ForeignKey(Products, related_name='replacement', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["origin", "replacement", "user"],
                name="unique_user_favoris",
            )
        ]

    def __str__(self):
        return str({
            "origin": self.origin,
            "replacement": self.replacement,
            "user": self.user
        })

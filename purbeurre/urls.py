from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search, name='search'),
    path('contacts/', views.contacts, name='contacts'),
    path('legal/', views.legal, name='legal'),
    path('<int:id_product>', views.detail, name='product_detail'),
]

from django.shortcuts import render, get_object_or_404, redirect
from .models import Products, Substitutes
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from users.models import User
from django.http import Http404


# Create your views here.

def index(request):
    context = {
        'page_title': 'Accueil'
    }
    return render(request, 'purbeurre/index.html')


def search(request):
    # query of the search product
    query = request.GET.get('query')

    # If query matches with product_name
    query_prod = Products.objects.filter(product_name__contains=query).first()

    # Check if the given string is contained in the value in database filed, query is not sensitive to case.
    if not query_prod:
        query_prod = Products.objects.filter(product_name__icontains=query).first()

    if not query_prod:
        # raise Http404("Poll does not exist")
        return redirect('purbeurre/404.html')
    else:
        products_list = Products.objects.filter(category=query_prod.category).filter(
            nutrition_score__lte=query_prod.nutrition_score).order_by('nutrition_score')
        # If user login is True
        if request.user.is_authenticated:
            # Remove products that are  already in the user's list
            for product in products_list:
                listed = Substitutes.objects.filter(
                    origin=query_prod.id_product,
                    replacement=product.id_product,
                    user=request.user
                )
                if listed:
                    products_list = products_list.exclude(pk=product.id_product)

    # If user wants to save a product
    if request.user.is_authenticated and request.method == 'POST':
        # product  searched
        origin = request.POST.get('origin')
        # get the replacement 
        replacement = request.POST.get('replacement')
        origin = Products.objects.get(pk=origin)
        replacement = Products.objects.get(pk=replacement)

        # Place the searched product and its alternative in the user's list
        Substitutes.objects.create(
            origin=origin,
            replacement=replacement,
            user=request.user
        )
        # exclude saved items from search results page
        products_list = products_list.exclude(pk=replacement.id_product)

    # pagination 9 products per page
    paginator = Paginator(products_list, 9)
    page = request.GET.get('page')

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    # Get the index of the current page
    page_index = products.number - 1
    # This value is maximum index of your pages, so the last page - 1
    max_index = len(paginator.page_range)
    # You want a range of 10, so lets calculate where to slice the list
    start_index = page_index - 10 if page_index >= 10 else 0
    end_index = page_index + 10 if page_index <= max_index - 10 else max_index
    # Get our new page range. In the latest versions of Django page_range returns 
    # an iterator. Thus pass it to list, to make our slice possible again.
    page_range = list(paginator.page_range)[start_index:end_index]

    context = {
        'products': products,
        'paginate': True,
        'query': query,
        'title': query_prod.product_name,
        'category': query_prod.category,
        'img': query_prod.img,
        'query_prod': query_prod.id_product,
        'page_range': page_range,

    }

    return render(request, 'purbeurre/search.html', context)


def detail(request, id_product):
    """
    detail information of each product
    """
    product = get_object_or_404(Products, pk=id_product)

    context = {
        "img": product.img,
        'product': product,
        "product_name": product.product_name
    }

    return render(request, 'purbeurre/product_detail.html', context)


# Contacts
def contacts(request):
    """
    contact page for the application
    """
    context = {
        "page_title": 'Nous contacter'
    }
    return render(request, 'purbeurre/contacts.html', context)


def legal(request):
    """
    legal page for the application
    """
    # Render
    context = {
        "title": "Mentions légales",
        "page_title": "Mentions légales"
    }
    return render(request, 'purbeurre/legal.html', context)

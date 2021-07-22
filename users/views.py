from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from purbeurre.models import Products, Substitutes
from purbeurre.forms import UserRegisterForm
from users.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages

# from django.contrib.auth import login, authenticate
# from purbeurre.forms import SignUpForm

# Create your views here.

def index(request):
    """ index page """
    context = {
        'page_title': 'Accueil'
    }
    return render(request, 'purbeurre/index.html')

def sign_up(request):
    """Display a register page and allow users to register"""
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(
                request,
                f"{username}: compte créé, vous pouvez vous connecter !",
            )
            return redirect("/users/account")
    else:
        form = UserRegisterForm()

    context = {
        "form": form,
        "title": "Créer un compte",
        "page_title": "S'enregistrer"
    }
    return render(request, "purbeurre/sign_up.html", context)

@login_required
def saved(request):
    products_saved = Substitutes.objects.filter(user=request.user.id).order_by('origin_id')

    # If user wants to delete a substitute product
    if request.user.is_authenticated and request.method == 'POST':
        origin = request.POST.get('origin')
        replacement = request.POST.get('replacement')
        user = User.objects.get(pk=request.user.id)
        
        origin = Products.objects.get(pk=origin)
        replacement = Products.objects.get(pk=replacement)

        # delete product from user's list
        Substitutes.objects.get(
            origin=origin,
            replacement=replacement,
            user=request.user
        ).delete()

    # Slice pages
    paginator = Paginator(products_saved, 5)  # show 5 items every page
    page = request.GET.get('page')

    try:
        products_saved = paginator.page(page)
    except PageNotAnInteger:
        products_saved = paginator.page(1)
    except EmptyPage:
        products_saved = paginator.page(paginator.num_pages)

    context = {
        "title": "Vos Favoris",
        "products_saved": products_saved,
        "paginate": True,
    }
    return render(request, 'purbeurre/saved.html', context)


@login_required
def account(request):
    """
    user profile page 
    """
    context = {
        "user": request.user,
        "page_title": 'Votre compte'
    }
    return render(request, 'purbeurre/account.html', context)

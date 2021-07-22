from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import User


class UserRegisterForm(UserCreationForm):
    """Customize register formulaire"""

    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "example@email.com",
            }
        ),
    )
    username = forms.CharField(
        label="Nom de l'utilisateur",
        widget=forms.TextInput(
            attrs={
                "placeholder": "nom d'utilisateur",
            }
        ),
    )

    password1 = forms.CharField(
        label="Mot de passe",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Mot de passe",
                "type": "password",
            }
        ),
    )

    password2 = forms.CharField(
        label="Confirmation de votre de passe",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Confirmation",
                "type": "password",
            }
        ),
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
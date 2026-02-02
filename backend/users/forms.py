from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Utilisateur

class InscriptionForm(UserCreationForm):
    first_name = forms.CharField(
        required=True,
        max_length=150,
        label="Prénom",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        })
    )

    last_name = forms.CharField(
        required=True,
        max_length=150,
        label="Nom",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        })
    )

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'votre@email.com'
        })
    )

    telephone = forms.CharField(
        required=False,
        max_length=15,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        })
    )

    adresse = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        })
    )

    class Meta:
        model = Utilisateur
        # ⚠️ ON RETIRE 'username' - il sera auto-généré
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2', 'telephone', 'adresse']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Mot de passe (min. 8 caractères)'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
        })

        # Ordre des champs
        self.order_fields(['first_name', 'last_name', 'email', 'password1', 'password2', 'telephone', 'adresse'])


class ConnexionForm(AuthenticationForm):
    # ⚠️ username = en fait l'EMAIL (Django l'appelle toujours username)
    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'votre@email.com'
        })
    )
    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Votre mot de passe'
        })
    )

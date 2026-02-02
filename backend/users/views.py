from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import InscriptionForm, ConnexionForm

def inscription(request):
    """Vue d'inscription d'un nouvel utilisateur"""
    if request.user.is_authenticated:
        return redirect('animaux:accueil')  # ← CORRIGÉ

    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Inscription réussie ! Bienvenue sur UniSpattes.')
            return redirect('animaux:accueil')  # ← CORRIGÉ
        else:
            messages.error(request, 'Erreur lors de l\'inscription. Veuillez vérifier vos informations.')
    else:
        form = InscriptionForm()

    return render(request, 'users/register.html', {'form': form})

def connexion(request):
    """Vue de connexion d'un utilisateur existant"""
    if request.user.is_authenticated:
        return redirect('animaux:accueil')  # ← CORRIGÉ

    if request.method == 'POST':
        form = ConnexionForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Bienvenue {user.first_name} !')
                return redirect('animaux:accueil')  # ← CORRIGÉ
        else:
            messages.error(request, 'Email ou mot de passe incorrect.')
    else:
        form = ConnexionForm()

    return render(request, 'users/login.html', {'form': form})

@login_required
def deconnexion(request):
    """Vue de déconnexion"""
    logout(request)
    messages.success(request, 'Vous avez été déconnecté avec succès.')
    return redirect('animaux:accueil')  # ← CORRIGÉ

@login_required
def profil(request):
    """Vue du profil utilisateur"""
    return render(request, 'users/profil.html', {'user': request.user})

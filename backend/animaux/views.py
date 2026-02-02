from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Animal, DemandeAdoption
from django.db import IntegrityError
from django.urls import reverse
from .forms import DemandeAdoptionForm

def index(request):
    animaux_recents = Animal.objects.all().order_by('-id')[:3]
    return render(request, 'animaux/index.html', {'animaux_recents': animaux_recents})

def nos_animaux(request):
    animaux = Animal.objects.all()
    return render(request, 'animaux/nos_animaux.html', {'animaux': animaux})

def detail_animal(request, id):
    """
    Affiche la fiche d'un animal.
    Le formulaire n'est traité QUE si l'utilisateur est connecté.
    """
    animal = get_object_or_404(Animal, id=id)

    # ✅ SI L'UTILISATEUR SOUMET LE FORMULAIRE SANS ÊTRE CONNECTÉ
    if request.method == 'POST' and not request.user.is_authenticated:
        messages.warning(
            request,
            "Vous devez être connecté pour envoyer une demande d'adoption."
        )
        return redirect(f"{reverse('users:connexion')}?next={request.path}")

    # Traitement formulaire (uniquement si connecté)
    if request.method == 'POST':
        form = DemandeAdoptionForm(request.POST)

        if form.is_valid():
            try:
                demande = form.save(commit=False)
                demande.animal = animal
                demande.utilisateur = request.user  # ✅ Associe l'utilisateur connecté
                demande.save()
                messages.success(
                    request,
                    f'Votre demande pour adopter {animal.nom} a bien été envoyée ! Nous vous recontacterons rapidement.'
                )
                return redirect('animaux:detail_animal', id=animal.id)

            except IntegrityError:
                messages.error(
                    request,
                    f'Vous avez déjà fait une demande pour {animal.nom}. '
                    'Consultez votre email ou contactez-nous.'
                )

        else:
            messages.error(
                request,
                "Veuillez corriger les erreurs ci-dessous avant de soumettre votre demande."
            )
            return render(request, 'animaux/detail_animal.html', {
                'animal': animal,
                'form': form,
                'scroll_to_errors': True
            })

    else:
        # GET → Formulaire vide (pré-rempli si connecté)
        if request.user.is_authenticated:
            form = DemandeAdoptionForm(initial={
                'animal': animal,
                'nom_complet': request.user.get_full_name(),
                'email': request.user.email
            })
        else:
            form = DemandeAdoptionForm(initial={'animal': animal})

    return render(request, 'animaux/detail_animal.html', {
        'animal': animal,
        'form': form
    })

def a_propos(request):
    """Page À propos"""
    return render(request, 'animaux/a_propos.html')

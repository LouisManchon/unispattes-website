from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Animal, DemandeAdoption
from django.db import IntegrityError
from .forms import DemandeAdoptionForm

def index(request):
    animaux_recents = Animal.objects.all().order_by('-id')[:3]
    return render(request, 'animaux/index.html', {'animaux_recents': animaux_recents})

def nos_animaux(request):
    animaux = Animal.objects.all()
    return render(request, 'animaux/nos_animaux.html', {'animaux': animaux})

def detail_animal(request, id):
    animal = get_object_or_404(Animal, id=id)

    # Traitement formulaire
    if request.method == 'POST':
        form = DemandeAdoptionForm(request.POST)

        if form.is_valid():
            try:
                demande = form.save(commit=False)
                demande.animal = animal
                demande.save()
                messages.success(
                    request,
                    f'✅ Votre demande pour adopter {animal.nom} a bien été envoyée ! Nous vous recontacterons rapidement.'
                )
                return redirect('animaux:detail_animal', id=animal.id)

            except IntegrityError:  # SI DOUBLON DÉTECTÉ
                messages.error(
                    request,
                    f'⚠️ Vous avez déjà fait une demande pour {animal.nom}. '
                    'Consultez votre email ou contactez-nous.'
                )

        else:
            # ❌ FORMULAIRE INVALIDE → Afficher les erreurs
            messages.error(
                request,
                "⚠️ Veuillez corriger les erreurs ci-dessous avant de soumettre votre demande."
            )

            # 🎯 RETOURNE LE FORMULAIRE AVEC LES ERREURS + FLAG POUR SCROLL
            return render(request, 'animaux/detail_animal.html', {
                'animal': animal,
                'form': form,
                'scroll_to_errors': True  # ← Pour activer le scroll JavaScript
            })

    else:
        # GET → Formulaire vide
        form = DemandeAdoptionForm(initial={'animal': animal})

    return render(request, 'animaux/detail_animal.html', {
        'animal': animal,
        'form': form
    })

def a_propos(request):
    """Page À propos"""
    return render(request, 'animaux/a_propos.html')

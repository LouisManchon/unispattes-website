from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Animal, DemandeAdoption
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
            demande = form.save(commit=False)
            demande.animal = animal
            demande.save()
            messages.success(request, f'✅ Demande pour {animal.nom} envoyée !')
            return redirect('detail_animal', id=animal.id)
    else:
        form = DemandeAdoptionForm(initial={'animal': animal})

    return render(request, 'animaux/detail_animal.html', {
        'animal': animal,
        'form': form
    })

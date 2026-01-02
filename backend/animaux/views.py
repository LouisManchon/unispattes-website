from django.shortcuts import render, get_object_or_404
from .models import Animal

def index(request):
    # Récupère les 3 animaux les plus récents
    animaux_recents = Animal.objects.all().order_by('-id')[:3]

    context = {
        'animaux_recents': animaux_recents
    }
    return render(request, 'animaux/index.html', context)

def nos_animaux(request):
    animaux = Animal.objects.all()
    context = {
        'animaux': animaux
    }
    return render(request, 'animaux/nos_animaux.html', context)

def detail_animal(request, id):
    """Affiche la page de détail d'un animal spécifique"""
    animal = get_object_or_404(Animal, id=id)
    context = {
        'animal': animal
    }
    return render(request, 'animaux/detail_animal.html', context)

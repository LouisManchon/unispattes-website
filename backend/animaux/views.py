from django.shortcuts import render
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

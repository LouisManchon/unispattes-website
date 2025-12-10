from django.shortcuts import render

def index(request):
    """Page d'accueil"""
    return render(request, 'animaux/index.html')

def nos_animaux(request):
    """Page listant tous les animaux"""
    return render(request, 'animaux/nos_animaux.html')

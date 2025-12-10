from django.shortcuts import render

def index(request):
    return render(request, 'animaux/index.html')

def nos_animaux(request):
    return render(request, 'animaux/nos_animaux.html')

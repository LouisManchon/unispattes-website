from django.urls import path
from . import views

app_name = 'animaux'

urlpatterns = [
    # Page d'accueil
    path('', views.index, name='accueil'),

    # Page affichant tous les animaux disponibles
    path('nos-animaux/', views.nos_animaux, name='nos_animaux'),

    # Fiche détaillée d’un animal
    path('animal/<int:id>/', views.detail_animal, name='detail_animal'),

    # Page de présentation du refuge
    path('a-propos/', views.a_propos, name='a_propos'),
]

from django.urls import path
from . import views

app_name = 'animaux'

urlpatterns = [
    # Page d'accueil
    path('', views.index, name='accueil'),

    # Liste des animaux
    path('nos-animaux/', views.nos_animaux, name='nos_animaux'),

    # Détails d'un animal
    path('animal/<int:id>/', views.detail_animal, name='detail_animal'),

    path('a-propos/', views.a_propos, name='a_propos'),
]

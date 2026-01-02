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

    # Formulaire d'adoption a faire quand la page sera faite
    # path('formulaire-adoption/<int:id>/', views.formulaire_adoption, name='formulaire_adoption')
]

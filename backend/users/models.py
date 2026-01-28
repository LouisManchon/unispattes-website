from django.contrib.auth.models import AbstractUser
from django.db import models

class Utilisateur(AbstractUser):
    """Utilisateur du refuge"""

    email = models.EmailField(unique=True, verbose_name="Email")
    telephone = models.CharField(max_length=15, blank=True, verbose_name="Téléphone")
    adresse = models.TextField(blank=True, verbose_name="Adresse")
    date_inscription = models.DateTimeField(auto_now_add=True)

    # Champs de sécurité manuels (que tu peux expliquer)
    tentatives_connexion = models.IntegerField(default=0, verbose_name="Tentatives échouées")
    compte_verrouille = models.BooleanField(default=False, verbose_name="Compte bloqué")

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"

    def __str__(self):
        return f"{self.username} ({self.email})"

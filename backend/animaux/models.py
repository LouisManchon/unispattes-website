from django.db import models

class Animal(models.Model):
    """Modèle représentant un animal"""

    # Choix pour le sexe de l'animal
    SEXE_CHOICES = [
        ('M', 'Mâle'),
        ('F', 'Femelle'),
    ]

    # Choix pour l'espèce de l'animal
    ESPECE_CHOICES = [
        ('CHIEN', 'Chien'),
        ('CHAT', 'Chat')
    ]

    # Choix pour la catégorie d'âge de l'animal
    CATEGORIE_AGE_CHOICES = [
        ('junior', 'Junior (moins de 2 ans)'),
        ('adulte', 'Adulte (2 à 7 ans)'),
        ('senior', 'Senior (plus de 7 ans)'),
    ]


    # Champs du modèle Animal
    nom = models.CharField(max_length=100, verbose_name="Nom")
    espece = models.CharField(max_length=10, choices=ESPECE_CHOICES, verbose_name="Espèce")
    age_annees = models.IntegerField(verbose_name="Âge (années)")
    age_mois = models.IntegerField(default=0, verbose_name="Âge (mois supplémentaires)")
    categorie_age = models.CharField(
        max_length=10,
        choices=CATEGORIE_AGE_CHOICES,
        verbose_name="Catégorie d'âge"
    )
    sexe = models.CharField(max_length=1, choices=SEXE_CHOICES, verbose_name="Sexe")
    race = models.CharField(max_length=100, blank=True, verbose_name="Race")
    description = models.TextField(verbose_name="Description")
    photo = models.ImageField(upload_to='animaux/', verbose_name="Photo")
    date_arrivee = models.DateField(auto_now_add=True, verbose_name="Date d'arrivée")
    disponible = models.BooleanField(default=True, verbose_name="Disponible à l'adoption")

    class Meta:
        verbose_name = "Animal"
        verbose_name_plural = "Animaux"
        ordering = ['-date_arrivee'] #  Les plus récents en premier

    def __str__(self):
        return f"{self.nom} ({self.get_espece_display()})"

    def get_age_display(self):
        """Retourne l'âge formaté (ex: '1 an', '10 mois', '5 ans')"""
        if self.age_annees == 0:
            return f"{self.age_mois} mois"
        elif self.age_mois == 0:
            return f"{self.age_annees} an" if self.age_annees == 1 else f"{self.age_annees} ans"
        else:
            return f"{self.age_annees} an{'s' if self.age_annees > 1 else ''} et {self.age_mois} mois"

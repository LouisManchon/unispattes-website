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

    def get_symbole_sexe(self):
        """Retourne le symbole du sexe (♂ ou ♀)"""
        return '♂' if self.sexe == 'M' else '♀'


# ========================================
# MODÈLE DEMANDE D'ADOPTION
# ========================================

class DemandeAdoption(models.Model):
    """Modèle représentant une demande d'adoption"""

    # Choix pour le type de logement
    TYPE_LOGEMENT_CHOICES = [
        ('MAISON_JARDIN', 'Maison avec jardin'),
        ('MAISON_SANS_JARDIN', 'Maison sans jardin'),
        ('APPARTEMENT_BALCON', 'Appartement avec balcon'),
        ('APPARTEMENT_SANS_BALCON', 'Appartement sans balcon'),
    ]

    # Choix pour le statut propriétaire/locataire
    STATUT_LOGEMENT_CHOICES = [
        ('PROPRIETAIRE', 'Propriétaire'),
        ('LOCATAIRE', 'Locataire (autorisation du propriétaire)'),
    ]

    # Choix pour les disponibilités
    CHOIX_DISPONIBILITE = [
        ('CETTE_SEMAINE', 'Cette semaine'),
        ('1_SEMAINE', 'Dans 1 semaine'),
        ('2_SEMAINES', 'Dans 2 semaines'),
        ('1_MOIS', 'Dans 1 mois'),
        ('FLEXIBLE', 'Flexible'),
    ]

    # ========================================
    # RELATIONS
    # ========================================
    animal = models.ForeignKey(
        Animal,
        on_delete=models.CASCADE,
        related_name='demandes_adoption',
        verbose_name="Animal"
    )

    # ========================================
    # INFORMATIONS ADOPTANT
    # ========================================
    nom_complet = models.CharField(
        max_length=200,
        verbose_name="Nom complet"
    )

    email = models.EmailField(
        verbose_name="Email"
    )

    telephone = models.CharField(
        max_length=20,
        verbose_name="Téléphone",
        help_text="Format: 06 12 34 56 78 ou 0612345678"
    )

    adresse = models.CharField(
        max_length=300,
        blank=True,
        verbose_name="Adresse complète (optionnel)"
    )

    # ========================================
    # INFORMATIONS LOGEMENT
    # ========================================
    type_logement = models.CharField(
        max_length=30,
        choices=TYPE_LOGEMENT_CHOICES,
        verbose_name="Type de logement"
    )

    statut_logement = models.CharField(
        max_length=20,
        choices=STATUT_LOGEMENT_CHOICES,
        verbose_name="Statut du logement"
    )

    # ========================================
    # AUTRES ANIMAUX
    # ========================================
    a_autres_animaux = models.BooleanField(
        default=False,
        verbose_name="Possède d'autres animaux"
    )

    details_autres_animaux = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Si oui, lesquels ?",
        help_text="Ex: 1 chat, 1 lapin"
    )

    # ========================================
    # MOTIVATION ET DISPONIBILITÉS
    # ========================================
    motivation = models.TextField(
        verbose_name="Pourquoi voulez-vous adopter cet animal ?",
        help_text="Minimum 50 caractères"
    )

    disponibilite = models.CharField(
        max_length=20,
        choices=CHOIX_DISPONIBILITE,
        default='FLEXIBLE',
        verbose_name="Quand pouvez-vous venir ?"
    )

    precisions_disponibilite = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Précisions sur vos disponibilités (optionnel)",
        help_text="Ex: Plutôt en fin d'après-midi"
    )

    # ========================================
    # MÉTADONNÉES
    # ========================================
    date_demande = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de la demande"
    )

    traitee = models.BooleanField(
        default=False,
        verbose_name="Demande traitée"
    )

    class Meta:
        verbose_name = "Demande d'adoption"
        verbose_name_plural = "Demandes d'adoption"
        ordering = ['-date_demande']  # Les plus récentes en premier

    def __str__(self):
        return f"Demande de {self.nom_complet} pour {self.animal.nom} ({self.date_demande.strftime('%d/%m/%Y')})"

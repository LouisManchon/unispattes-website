from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Animal, DemandeAdoption

Utilisateur = get_user_model()

class AnimauxTests(TestCase):

    def setUp(self):
        # Création d'un utilisateur de test
        self.user = Utilisateur.objects.create_user(
            email='testuser@example.com',
            password='TestPassword123',
            first_name='Test',
            last_name='User'
        )
        # Création d'un animal de test
        self.animal = Animal.objects.create(
            nom='Charlie',
            espece='CHIEN',
            age_annees=3,
            age_mois=6,
            categorie_age='adulte',
            sexe='M',
            race='Labrador',
            description='Un chien très affectueux.',
            photo='animaux/test.jpg',
            disponible=True
        )

    def test_nos_animaux_page(self):
        """Vérifie que la page liste des animaux s'affiche correctement"""
        response = self.client.get(reverse('animaux:nos_animaux'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.animal.nom)

    def test_detail_animal_page(self):
        """Vérifie que la page détail d'un animal s'affiche correctement"""
        response = self.client.get(reverse('animaux:detail_animal', args=[self.animal.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.animal.nom)
        self.assertContains(response, self.animal.description)

    def test_creation_demande_adoption(self):
        """Vérifie qu'un utilisateur connecté peut créer une demande d'adoption"""
        self.client.login(email='testuser@example.com', password='TestPassword123')
        form_data = {
            'nom_complet': f'{self.user.first_name} {self.user.last_name}',
            'email': self.user.email,
            'telephone': '0612345678',
            'adresse': '123 rue du Test',
            'type_logement': 'MAISON_JARDIN',
            'statut_logement': 'PROPRIETAIRE',
            'a_autres_animaux': False,
            'details_autres_animaux': '',
            'motivation': 'J’adore les chiens et souhaite offrir un foyer aimant.',
            'disponibilite': 'CETTE_SEMAINE',
            'precisions_disponibilite': ''
        }
        response = self.client.post(
            reverse('animaux:detail_animal', args=[self.animal.id]),
            data=form_data
        )
        # Vérifie la redirection après succès
        self.assertEqual(response.status_code, 302)
        # Vérifie que la demande a été créée
        self.assertTrue(DemandeAdoption.objects.filter(
            utilisateur=self.user,
            animal=self.animal
        ).exists())

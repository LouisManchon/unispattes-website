from django.test import TestCase
from django.urls import reverse
from .models import Utilisateur

class UtilisateurTests(TestCase):
    def setUp(self):
        # Création d'un utilisateur de test
        self.user = Utilisateur.objects.create_user(
            email='testuser@example.com',
            password='TestPassword123',
            first_name='Test',
            last_name='User'
        )

    def test_inscription_utilisateur(self):
        response = self.client.post(reverse('users:inscription'), {
            'first_name': 'Nouvel',
            'last_name': 'Utilisateur',
            'email': 'newuser@example.com',
            'password1': 'Password123!',
            'password2': 'Password123!',
            'telephone': '0123456789',
            'adresse': '1 rue Test'
        })
        # Vérifie redirection
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('animaux:accueil'))
        # Vérifie création utilisateur
        self.assertTrue(Utilisateur.objects.filter(email='newuser@example.com').exists())

    def test_connexion_utilisateur(self):
        response = self.client.post(reverse('users:connexion'), {
            'username': 'testuser@example.com',  # email utilisé comme username
            'password': 'TestPassword123'
        })
        # Vérifie redirection
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('animaux:accueil'))
        # Vérifie que l'utilisateur est authentifié
        self.assertTrue('_auth_user_id' in self.client.session)

from django import forms
from .models import DemandeAdoption


class DemandeAdoptionForm(forms.ModelForm):
    """
    Formulaire de demande d'adoption
    Validation souple pour développement
    """

    class Meta:
        model = DemandeAdoption
        fields = [
            'animal',
            'nom_complet',
            'email',
            'telephone',
            'adresse',
            'type_logement',
            'statut_logement',
            'superficie',
            'a_jardin',
            'superficie_jardin',
            'a_experience',
            'description_experience',
            'a_autres_animaux',
            'details_autres_animaux',
            'motivation',
            'disponibilite',
            'precisions_disponibilite',
        ]

        widgets = {
            'animal': forms.HiddenInput(),  # Pré-rempli automatiquement

            # Textes simples
            'nom_complet': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Votre nom complet',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'votre@email.com',
            }),
            'telephone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '06 12 34 56 78',
            }),
            'adresse': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Votre adresse complète',
            }),

            # Sélections
            'type_logement': forms.Select(attrs={'class': 'form-select'}),
            'statut_logement': forms.Select(attrs={'class': 'form-select'}),
            'disponibilite': forms.Select(attrs={'class': 'form-select'}),

            # Nombres
            'superficie': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'En m²',
                'min': '0',
            }),
            'superficie_jardin': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'En m²',
                'min': '0',
            }),

            # Cases à cocher
            'a_jardin': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'a_experience': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'a_autres_animaux': forms.CheckboxInput(attrs={'class': 'form-check-input'}),

            # Zones de texte
            'description_experience': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Décrivez votre expérience avec les animaux...',
            }),
            'details_autres_animaux': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Quels animaux avez-vous ?',
            }),
            'motivation': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Pourquoi souhaitez-vous adopter cet animal ?',
            }),
            'precisions_disponibilite': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Précisions sur votre disponibilité...',
            }),
        }

        labels = {
            'nom_complet': '👤 Nom complet',
            'email': '📧 Email',
            'telephone': '📱 Téléphone',
            'adresse': '🏠 Adresse',
            'type_logement': '🏡 Type de logement',
            'statut_logement': '📋 Statut',
            'a_jardin': 'Avez-vous un jardin ?',
            'description_experience': '📝 Décrivez votre expérience',
            'a_autres_animaux': 'Avez-vous déjà d\'autres animaux ?',
            'details_autres_animaux': '🐾 Détails',
            'motivation': '💭 Motivation',
            'disponibilite': '⏰ Disponibilité',
            'precisions_disponibilite': '📝 Précisions',
        }

    def clean_email(self):
        """
        Validation souple de l'email (développement)
        """
        email = self.cleaned_data.get('email')

        # Accepte les emails de test
        if email and '@' not in email:
            # En mode DEV, on accepte quand même
            pass

        return email

    def clean_telephone(self):
        """
        Validation souple du téléphone (développement)
        """
        telephone = self.cleaned_data.get('telephone')

        # Accepte n'importe quel format en DEV
        return telephone

    def clean(self):
        """
        Validations croisées
        """
        cleaned_data = super().clean()

        # Logique : si jardin coché, demander la superficie
        a_jardin = cleaned_data.get('a_jardin')
        superficie_jardin = cleaned_data.get('superficie_jardin')

        if a_jardin and not superficie_jardin:
            # En DEV, on met une valeur par défaut
            cleaned_data['superficie_jardin'] = 0

        # Logique : si expérience cochée, demander la description
        a_experience = cleaned_data.get('a_experience')
        description_experience = cleaned_data.get('description_experience')

        if a_experience and not description_experience:
            # En DEV, on accepte
            pass

        return cleaned_data

from django import forms
from .models import DemandeAdoption


class DemandeAdoptionForm(forms.ModelForm):
    """Formulaire de demande d'adoption"""

    class Meta:
        model = DemandeAdoption
        fields = [
            'nom_complet',
            'email',
            'telephone',
            'adresse',
            'type_logement',
            'statut_logement',
            'a_autres_animaux',
            'details_autres_animaux',
            'motivation',
            'disponibilite',
            'precisions_disponibilite',
        ]

        widgets = {
            'nom_complet': forms.TextInput(attrs={
            }),
            'email': forms.EmailInput(attrs={
            }),
            'telephone': forms.TextInput(attrs={
                'placeholder': '06 12 34 56 78',
            }),
            'adresse': forms.TextInput(attrs={
            }),
            'type_logement': forms.Select(),
            'statut_logement': forms.Select(),
            'a_autres_animaux': forms.CheckboxInput(),
            'details_autres_animaux': forms.TextInput(attrs={
            }),
            'motivation': forms.Textarea(attrs={
                'rows': 5,
            }),
            'disponibilite': forms.Select(),
            'precisions_disponibilite': forms.TextInput(attrs={
                'placeholder': 'Ex: Plutôt en fin d\'après-midi',
            }),
        }

        labels = {
            'nom_complet': 'Nom et prénom',
            'email': 'Adresse email',
            'telephone': 'Numéro de téléphone',
            'adresse': 'Adresse (optionnel)',
            'type_logement': 'Type de logement',
            'statut_logement': 'Statut du logement',
            'a_autres_animaux': 'Possédez-vous d\'autres animaux ?',
            'details_autres_animaux': 'Si oui, lesquels ?',
            'motivation': 'Pourquoi voulez-vous adopter cet animal ?',
            'disponibilite': 'Quand pouvez-vous venir ?',
            'precisions_disponibilite': 'Précisions sur vos disponibilités (optionnel)',
        }

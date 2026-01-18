from django import forms
from .models import DemandeAdoption

class DemandeAdoptionForm(forms.ModelForm):
    """Formulaire de demande d'adoption"""

    type_logement = forms.ChoiceField(
        choices=DemandeAdoption.TYPE_LOGEMENT_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'radio-buttons'}),
        required=True,
        error_messages={'required': '⚠️ Veuillez sélectionner un type de logement.'}
    )

    statut_logement = forms.ChoiceField(
        choices=DemandeAdoption.STATUT_LOGEMENT_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'radio-buttons'}),
        required=True,
        error_messages={'required': '⚠️ Veuillez indiquer si vous êtes propriétaire ou locataire.'}
    )

    disponibilite = forms.ChoiceField(
        choices=DemandeAdoption.CHOIX_DISPONIBILITE,
        widget=forms.RadioSelect(attrs={'class': 'radio-buttons'}),
        required=True,
        error_messages={'required': '⚠️ Veuillez indiquer quand vous pouvez venir.'}
    )

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
                'class': 'form-control',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
            }),
            'telephone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '06 12 34 56 78',
            }),
            'adresse': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            # Checkbox stylisée
            'a_autres_animaux': forms.CheckboxInput(attrs={
                'class': 'custom-checkbox',
            }),
            'details_autres_animaux': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'motivation': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
            }),
            'precisions_disponibilite': forms.TextInput(attrs={
                'class': 'form-control',
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

    def clean_type_logement(self):
        """Valide que l'utilisateur a bien sélectionné un type de logement"""
        type_logement = self.cleaned_data.get('type_logement')
        if not type_logement:
            raise forms.ValidationError("⚠️ Veuillez sélectionner un type de logement.")
        return type_logement

    def clean_statut_logement(self):
        """Valide que l'utilisateur a bien sélectionné son statut"""
        statut_logement = self.cleaned_data.get('statut_logement')
        if not statut_logement:
            raise forms.ValidationError("⚠️ Veuillez indiquer si vous êtes propriétaire ou locataire.")
        return statut_logement

    def clean_disponibilite(self):
        """Valide que l'utilisateur a bien sélectionné ses disponibilités"""
        disponibilite = self.cleaned_data.get('disponibilite')
        if not disponibilite:
            raise forms.ValidationError("⚠️ Veuillez indiquer quand vous pouvez venir.")
        return disponibilite

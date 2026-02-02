from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import Utilisateur

def nombre_demandes(obj):
    """Compte le nombre de demandes d'adoption"""
    try:
        from animaux.models import DemandeAdoption
        return DemandeAdoption.objects.filter(utilisateur=obj).count()
    except Exception as e:
        return f"Erreur: {e}"
nombre_demandes.short_description = "📋 Demandes"


class DemandeAdoptionInline(admin.TabularInline):
    """Affiche l'historique des demandes d'adoption"""
    from animaux.models import DemandeAdoption
    model = DemandeAdoption
    extra = 0
    can_delete = False

    fields = (
        'animal_link',
        'date_demande',
        'statut_badge',
        'contact_info',
        'logement_info',
        'autres_animaux_info',
        'motivation_courte',
        'disponibilite_info'
    )

    readonly_fields = (
        'animal_link',
        'date_demande',
        'statut_badge',
        'contact_info',
        'logement_info',
        'autres_animaux_info',
        'motivation_courte',
        'disponibilite_info'
    )

    def animal_link(self, obj):
        """Lien vers l'animal"""
        if obj.animal:
            url = f"/admin/animaux/animal/{obj.animal.id}/change/"
            return format_html('<a href="{}">{}</a>', url, obj.animal.nom)
        return "-"
    animal_link.short_description = "Animal"

    def statut_badge(self, obj):
        """Badge coloré pour le statut"""
        couleurs = {
            'en_attente': '#FFA500',
            'approuvee': '#28A745',
            'refusee': '#DC3545'
        }
        labels = {
            'en_attente': 'En attente',
            'approuvee': 'Approuvée',
            'refusee': 'Refusée'
        }
        couleur = couleurs.get(obj.statut, '#6C757D')
        label = labels.get(obj.statut, obj.statut)
        return format_html(
            '<span style="background-color: {}; color: white; padding: 5px 10px; border-radius: 5px;">{}</span>',
            couleur, label
        )
    statut_badge.short_description = "Statut"

    def contact_info(self, obj):
        """Informations de contact"""
        return format_html(
            "<strong>Nom:</strong> {}<br>"
            "<strong>Email:</strong> {}<br>"
            "<strong>Téléphone:</strong> {}<br>"
            "<strong>Adresse:</strong> {}",
            obj.nom_complet or "-",
            obj.email or "-",
            obj.telephone or "-",
            obj.adresse or "Non renseignée"
        )
    contact_info.short_description = "Contact"

    def logement_info(self, obj):
        """Informations sur le logement"""
        return format_html(
            "<strong>Type:</strong> {}<br>"
            "<strong>Statut:</strong> {}",
            obj.get_type_logement_display() if obj.type_logement else "-",
            obj.get_statut_logement_display() if obj.statut_logement else "-"
        )
    logement_info.short_description = "Logement"

    def autres_animaux_info(self, obj):
        """Informations sur les autres animaux"""
        if obj.a_autres_animaux:
            return format_html(
                "<strong>Oui</strong><br>"
                "{}",
                obj.details_autres_animaux or "Détails non précisés"
            )
        return "Non"
    autres_animaux_info.short_description = "Autres animaux"

    def motivation_courte(self, obj):
        """Motivation"""
        if obj.motivation:
            return obj.motivation[:80] + "..." if len(obj.motivation) > 80 else obj.motivation
        return "-"
    motivation_courte.short_description = "Motivation"

    def disponibilite_info(self, obj):
        """Disponibilités"""
        dispo = obj.get_disponibilite_display() if obj.disponibilite else "-"
        precisions = f"<br><em>{obj.precisions_disponibilite}</em>" if obj.precisions_disponibilite else ""
        return format_html(
            "<strong>Quand:</strong> {}{}",
            dispo,
            precisions
        )
    disponibilite_info.short_description = "Disponibilité"


@admin.register(Utilisateur)
class UtilisateurAdmin(UserAdmin):
    """Interface admin pour les utilisateurs"""

    list_display = (
        'email',
        'first_name',
        'last_name',
        'is_staff',
        'date_inscription',
        nombre_demandes,
        'compte_verrouille'
    )

    list_filter = ('is_staff', 'is_superuser', 'compte_verrouille', 'date_inscription')
    search_fields = ('email', 'first_name', 'last_name', 'telephone')

    fieldsets = (
        ('🔐 Identification', {
            'fields': ('email', 'password')
        }),
        ('👤 Informations personnelles', {
            'fields': ('first_name', 'last_name', 'telephone', 'adresse')
        }),
        ('🔒 Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('🔒 Sécurité', {
            'fields': ('tentatives_connexion', 'compte_verrouille', 'date_inscription')
        }),
    )

    readonly_fields = ('date_inscription',)
    ordering = ('email',)

    # L'inline qui affiche les demandes
    inlines = [DemandeAdoptionInline]

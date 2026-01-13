from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import Animal, DemandeAdoption


# ========================================
# ADMIN ANIMAL
# ========================================
@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ('nom', 'espece', 'race', 'get_age_display', 'sexe', 'disponible', 'date_arrivee')
    list_filter = ('espece', 'sexe', 'disponible', 'categorie_age')
    search_fields = ('nom', 'race', 'description')
    list_editable = ('disponible',)
    readonly_fields = ('date_arrivee',)

    fieldsets = (
        ('Informations générales', {
            'fields': ('nom', 'espece', 'race', 'sexe')
        }),
        ('Âge', {
            'fields': ('age_annees', 'age_mois', 'categorie_age')
        }),
        ('Description', {
            'fields': ('description', 'photo')
        }),
        ('Statut', {
            'fields': ('disponible', 'date_arrivee')
        }),
    )

    def get_age_display(self, obj):
        return obj.get_age_display()
    get_age_display.short_description = 'Âge'


# ========================================
# ADMIN DEMANDE D'ADOPTION
# ========================================
@admin.register(DemandeAdoption)
class DemandeAdoptionAdmin(admin.ModelAdmin):
    """
    Interface admin pour gérer les demandes d'adoption
    """

    # ========================================
    # LISTE DES DEMANDES
    # ========================================
    list_display = (
        'get_numero_demande',
        'nom_complet',
        'animal',
        'get_type_logement_emoji',
        'get_date_demande_courte',
        'disponibilite',
        'telephone',
        'traitee',
        'statut_colored',
    )

    # ========================================
    # FILTRES
    # ========================================
    list_filter = (
        'traitee',
        'date_demande',
        'animal__espece',
        'type_logement',
        'statut_logement',
        'a_autres_animaux',
        'disponibilite',
    )

    # ========================================
    # RECHERCHE
    # ========================================
    search_fields = (
        'nom_complet',
        'email',
        'telephone',
        'animal__nom',
        'motivation',
    )

    list_editable = ('traitee',)
    readonly_fields = ('date_demande', 'get_numero_demande')
    date_hierarchy = 'date_demande'
    list_per_page = 25

    # ========================================
    # MÉTHODES PERSONNALISÉES
    # ========================================

    def get_numero_demande(self, obj):
        """Numéro formaté"""
        return f"#{obj.id:05d}"
    get_numero_demande.short_description = '🔢 N°'
    get_numero_demande.admin_order_field = 'id'

    def get_type_logement_emoji(self, obj):
        """Type de logement avec emoji"""
        emoji_map = {
            'MAISON_JARDIN': '🏡🌿',
            'MAISON_SANS_JARDIN': '🏠',
            'APPARTEMENT_BALCON': '🏢🌿',
            'APPARTEMENT_SANS_BALCON': '🏢',
        }
        emoji = emoji_map.get(obj.type_logement, '❓')
        label = obj.get_type_logement_display().split(' ')[0]
        return f"{emoji} {label}"
    get_type_logement_emoji.short_description = '🏠 Logement'
    get_type_logement_emoji.admin_order_field = 'type_logement'

    def get_date_demande_courte(self, obj):
        """Date avec SLA : 48h pour répondre"""
        delta = timezone.now() - obj.date_demande
        heures = delta.total_seconds() / 3600

        # Si déjà traitée → pas d'alerte
        if obj.traitee:
            if delta.days == 0:
                return f"Auj. {obj.date_demande.strftime('%H:%M')}"
            elif delta.days == 1:
                return f"Hier {obj.date_demande.strftime('%H:%M')}"
            else:
                return obj.date_demande.strftime('%d/%m')

        # Si non traitée → SLA
        if heures < 24:
            return format_html(
                '<span style="color: green;">🟢 {} ({}h)</span>',
                "Aujourd'hui" if delta.days == 0 else "Hier",
                int(heures)
            )
        elif heures < 48:
            return format_html(
                '<span style="color: orange;">⚠️ {}h restantes (SLA)</span>',
                48 - int(heures)
            )
        else:
            jours = delta.days
            return format_html(
                '<span style="color: red; font-weight: bold;">🔴 RETARD {}j !</span>',
                jours
            )
    get_date_demande_courte.short_description = "Date / SLA"
    get_date_demande_courte.admin_order_field = 'date_demande'

    def statut_colored(self, obj):
        """Statut avec emoji"""
        if obj.traitee:
            return "✅ Traitée"
        return "⏳ En attente"
    statut_colored.short_description = '📋 Statut'
    statut_colored.admin_order_field = 'traitee'

    # ========================================
    # ACTIONS GROUPÉES
    # ========================================
    actions = ['marquer_comme_traitee', 'marquer_comme_non_traitee']

    @admin.action(description="✅ Marquer comme traitée")
    def marquer_comme_traitee(self, request, queryset):
        count = queryset.update(traitee=True)
        self.message_user(request, f"{count} demande(s) marquée(s) comme traitée(s).")

    @admin.action(description="⏳ Marquer comme non traitée")
    def marquer_comme_non_traitee(self, request, queryset):
        count = queryset.update(traitee=False)
        self.message_user(request, f"{count} demande(s) marquée(s) comme non traitée(s).")

    # ========================================
    # FORMULAIRE DÉTAILLÉ
    # ========================================
    fieldsets = (
        ('🔢 Identification', {
            'fields': ('get_numero_demande', 'animal', 'date_demande')
        }),

        ('👤 Informations personnelles', {
            'fields': ('nom_complet', 'email', 'telephone', 'adresse')
        }),

        ('🏠 Logement', {
            'fields': (
                'type_logement',
                'statut_logement',
            )
        }),

        ('🐾 Expérience avec les animaux', {
            'fields': (
                'a_autres_animaux',
                'details_autres_animaux',
            )
        }),

        ('💭 Motivation et disponibilité', {
            'fields': (
                'motivation',
                'disponibilite',
                'precisions_disponibilite',
            )
        }),

        ('📋 Traitement', {
            'fields': ('traitee', 'notes_admin'),
            'classes': ('collapse',),
        }),
    )

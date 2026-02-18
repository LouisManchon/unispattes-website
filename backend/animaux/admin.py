from django.contrib import admin
from django.utils.html import format_html
from django.shortcuts import get_object_or_404, redirect
from django.urls import path
from django.shortcuts import redirect
from django.contrib import messages
from .models import Animal, DemandeAdoption
from django.utils.safestring import mark_safe


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
    """Interface admin pour gérer les demandes d'adoption"""

    # ========================================
    # LISTE DES DEMANDES
    # ========================================
    list_display = (
        'get_numero_demande',
        'nom_complet',
        'animal',
        'get_type_logement_emoji',
        'get_date_demande',
        'telephone',
        'get_statut_colored',
        'get_boutons_action',
    )

    # ========================================
    # FILTRES
    # ========================================
    list_filter = (
        'statut',
        'date_demande',
        'animal__espece',
        'type_logement',
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

    readonly_fields = ('date_demande', 'get_numero_demande')
    date_hierarchy = 'date_demande'
    list_per_page = 25

    # ========================================
    # COLONNES PERSONNALISÉES
    # ========================================

    def get_numero_demande(self, obj):
        """Numéro formaté"""
        return f"#{obj.id:05d}"
    get_numero_demande.short_description = '🔢 N°'
    get_numero_demande.admin_order_field = 'id'

    def get_type_logement_emoji(self, obj):
        """Type de logement avec emoji"""
        emoji_map = {
            'MAISON_JARDIN': '🏡',
            'MAISON_SANS_JARDIN': '🏠',
            'APPARTEMENT_BALCON': '🏢🌿',
            'APPARTEMENT_SANS_BALCON': '🏢',
        }
        emoji = emoji_map.get(obj.type_logement, '❓')
        return f"{emoji} {obj.get_type_logement_display()}"
    get_type_logement_emoji.short_description = '🏠 Logement'

    def get_date_demande(self, obj):
        """Date formatée simplement"""
        return obj.date_demande.strftime('%d/%m/%Y à %H:%M')
    get_date_demande.short_description = '📅 Date de demande'
    get_date_demande.admin_order_field = 'date_demande'

    def get_statut_colored(self, obj):
        """Statut avec couleur"""
        couleurs = {
            'EN_ATTENTE': ('background:#fff3cd;color:#856404;', '⏳ En attente'),
            'ACCEPTEE': ('background:#d4edda;color:#155724;', '✅ Acceptée'),
            'REFUSEE': ('background:#f8d7da;color:#721c24;', '❌ Refusée'),
        }
        style, texte = couleurs.get(obj.statut, ('', obj.get_statut_display()))
        return format_html(
            '<span style="padding:6px 12px;border-radius:6px;font-weight:600;display:inline-block;{}">{}</span>',
            style, texte
        )
    get_statut_colored.short_description = '📊 Statut'
    get_statut_colored.admin_order_field = 'statut'

    def get_boutons_action(self, obj):
        """Boutons rapides Accepter/Refuser"""
        if obj.statut == 'EN_ATTENTE':
            return mark_safe(
                f'<a href="{obj.pk}/accepter/" style="background:#28a745;color:white;padding:6px 12px;'
                f'border-radius:6px;text-decoration:none;margin-right:5px;display:inline-block;'
                f'font-size:12px;font-weight:600;">✅ Accepter</a>'
                f'<a href="{obj.pk}/refuser/" style="background:#dc3545;color:white;padding:6px 12px;'
                f'border-radius:6px;text-decoration:none;display:inline-block;'
                f'font-size:12px;font-weight:600;">❌ Refuser</a>'
            )
        elif obj.statut == 'ACCEPTEE':
            return mark_safe('<span style="color:#28a745;font-weight:600;">✅ Adoption validée</span>')
        else:
            return mark_safe('<span style="color:#dc3545;font-weight:600;">❌ Refusée</span>')

    get_boutons_action.short_description = '⚡ Actions'





    # ========================================
    # ACTIONS GROUPÉES
    # ========================================
    actions = ['accepter_demandes', 'refuser_demandes', 'remettre_en_attente']

    @admin.action(description="✅ Accepter les demandes sélectionnées")
    def accepter_demandes(self, request, queryset):
        count = 0
        for demande in queryset.filter(statut='EN_ATTENTE'):
            demande.statut = 'ACCEPTEE'
            demande.traitee = True
            demande.animal.disponible = False
            demande.animal.save()
            demande.save()
            count += 1
        self.message_user(request, f"✅ {count} demande(s) acceptée(s). Animaux marqués comme indisponibles.", messages.SUCCESS)

    @admin.action(description="❌ Refuser les demandes sélectionnées")
    def refuser_demandes(self, request, queryset):
        count = queryset.filter(statut='EN_ATTENTE').update(statut='REFUSEE', traitee=True)
        self.message_user(request, f"❌ {count} demande(s) refusée(s).", messages.WARNING)

    @admin.action(description="⏳ Remettre en attente")
    def remettre_en_attente(self, request, queryset):
        count = queryset.update(statut='EN_ATTENTE', traitee=False)
        self.message_user(request, f"⏳ {count} demande(s) remise(s) en attente.")

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
            'fields': ('type_logement', 'statut_logement')
        }),

        ('🐾 Expérience avec les animaux', {
            'fields': ('a_autres_animaux', 'details_autres_animaux')
        }),

        ('💭 Motivation et disponibilité', {
            'fields': ('motivation', 'disponibilite', 'precisions_disponibilite')
        }),

        ('📋 Statut et traitement', {
            'fields': ('statut', 'traitee', 'notes_admin'),
        }),
    )

    # ========================================
    # URLS PERSONNALISÉES POUR LES BOUTONS
    # ========================================
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:pk>/accepter/', self.admin_site.admin_view(self.accepter_demande), name='animaux_demandeadoption_accepter'),
            path('<int:pk>/refuser/', self.admin_site.admin_view(self.refuser_demande), name='animaux_demandeadoption_refuser'),
        ]
        return custom_urls + urls

    def accepter_demande(self, request, pk):
        """✅ Accepter une demande"""
        try:
            demande = get_object_or_404(DemandeAdoption, pk=pk)

            # ✅ Vérifier que la demande est en attente
            if demande.statut != 'EN_ATTENTE':
                messages.warning(request, f"⚠️ Cette demande a déjà été traitée (statut : {demande.get_statut_display()}).")
                return redirect('admin:animaux_demandeadoption_changelist')

            # 🔥 NOUVEAU : Vérifier que l'animal est encore disponible
            if not demande.animal.disponible:
                messages.error(
                    request,
                    f"❌ Impossible d'accepter cette demande : {demande.animal.nom} a déjà été adopté !"
                )
                return redirect('admin:animaux_demandeadoption_changelist')

            # ✅ Accepter la demande
            demande.statut = 'ACCEPTEE'
            demande.traitee = True
            demande.save()

            # ✅ Marquer l'animal comme indisponible
            demande.animal.disponible = False
            demande.animal.save()

            messages.success(
                request,
                f"✅ Demande #{demande.id:05d} acceptée ! {demande.animal.nom} est maintenant indisponible à l'adoption."
            )

        except Exception as e:
            messages.error(request, f"❌ Erreur : {str(e)}")

        return redirect('admin:animaux_demandeadoption_changelist')


    def refuser_demande(self, request, pk):
        """❌ Refuser une demande"""
        demande = DemandeAdoption.objects.get(pk=pk)
        demande.statut = 'REFUSEE'
        demande.traitee = True
        demande.save()

        messages.warning(request, f"❌ Demande de {demande.nom_complet} refusée.")
        return redirect('admin:animaux_demandeadoption_changelist')

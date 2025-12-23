from django.contrib import admin
from .models import Animal

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

    # Pour que get_age_display s'affiche avec un titre personnalisé
    def get_age_display(self, obj):
        return obj.get_age_display()
    get_age_display.short_description = 'Âge'

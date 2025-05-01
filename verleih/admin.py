from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Person, Asset, Ausleihe, Rueckgabe

admin.site.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('teilnehmer_id', 'name', 'projekt')
    search_fields = ('name', 'teilnehmer_id')
admin.site.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('asset_tag', 'asset_name', 'model', 'category', 'status', 'location')
    search_fields = ('asset_tag', 'asset_name', 'model')
admin.site.register(Ausleihe)
class AusleiheAdmin(admin.ModelAdmin):
    list_display = ('person', 'asset', 'timestamp', 'user')
    search_fields = ('person__name', 'asset__asset_tag')
admin.site.register(Rueckgabe)
class RueckgabeAdmin(admin.ModelAdmin):
    list_display = ('ausleihe', 'zustand', 'kommentar', 'timestamp', 'user')
    search_fields = ('ausleihe__person__name', 'ausleihe__asset__asset_tag')

Group.objects.get_or_create(name="Menti")
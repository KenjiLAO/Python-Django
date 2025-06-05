# admin.py
from django.contrib import admin
from .models import Article

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('titre', 'statut', 'auteur', 'date_creation')
    list_filter = ('statut',)
    search_fields = ('titre', 'contenu')

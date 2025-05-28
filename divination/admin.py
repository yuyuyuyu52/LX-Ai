from django.contrib import admin
from .models import TarotCard, IChingHexagram, BaziElement

@admin.register(TarotCard)
class TarotCardAdmin(admin.ModelAdmin):
    list_display = ('name', 'suit', 'card_number')
    list_filter = ('suit',)
    search_fields = ('name', 'name_en')
    ordering = ('suit', 'card_number', 'name')

@admin.register(IChingHexagram)
class IChingHexagramAdmin(admin.ModelAdmin):
    list_display = ('number', 'name', 'chinese_name')
    search_fields = ('name', 'chinese_name', 'meaning')
    ordering = ('number',)

@admin.register(BaziElement)
class BaziElementAdmin(admin.ModelAdmin):
    list_display = ('name', 'element_type', 'wuxing')
    list_filter = ('element_type', 'wuxing')
    search_fields = ('name',)
    ordering = ('element_type', 'name')

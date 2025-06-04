from django.contrib import admin
from .models import BaziElement

@admin.register(BaziElement)
class BaziElementAdmin(admin.ModelAdmin):
    list_display = ('name', 'element_type', 'wuxing')
    list_filter = ('element_type', 'wuxing')
    search_fields = ('name',)
    ordering = ('element_type', 'name')

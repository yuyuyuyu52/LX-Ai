from django.contrib import admin
from .models import ChineseCalendarDay, SolarTerm

@admin.register(ChineseCalendarDay)
class ChineseCalendarDayAdmin(admin.ModelAdmin):
    list_display = ('date', 'lunar_year', 'lunar_month', 'lunar_day')
    list_filter = ('lunar_month',)
    search_fields = ('date', 'lunar_year')
    date_hierarchy = 'date'
    ordering = ('-date',)

@admin.register(SolarTerm)
class SolarTermAdmin(admin.ModelAdmin):
    list_display = ('name', 'date')
    search_fields = ('name', 'description')
    ordering = ('date',)

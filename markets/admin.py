from django.contrib import admin
from markets.models import Markets


@admin.register(Markets)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['market_name']
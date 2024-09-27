from django.contrib import admin
from markets.models import Market


@admin.register(Market)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['market_name']
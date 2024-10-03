from django.contrib import admin
from markets.models import Market, MkImage


@admin.register(Market)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'market_name', 'additional_name']
    ordering = ['market_name', 'additional_name']


@admin.register(MkImage)
class MkImageAdmin(admin.ModelAdmin):
    list_display = ['market', 'image']
    list_filter = ['market']
    ordering = ['market']

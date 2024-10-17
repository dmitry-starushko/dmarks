from django.contrib import admin
from markets.models import *


@admin.register(Market)
class MarketAdmin(admin.ModelAdmin):
    list_display = ['id', 'market_name', 'additional_name']
    ordering = ['market_name', 'additional_name']


@admin.register(SvgSchema)
class SvgSchemaAdmin(admin.ModelAdmin):
    list_display = ['id', 'market', 'floor', 'descr']
    list_filter = ['market']
    ordering = ['market', 'floor']


@admin.register(MkImage)
class MkImageAdmin(admin.ModelAdmin):
    list_display = ['market', 'image']
    list_filter = ['market']
    ordering = ['market']

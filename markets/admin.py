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


@admin.register(GlobalConfig)
class GlobalConfigAdmin(admin.ModelAdmin):
    list_display = ['param_name', 'param_data', 'descr']
    ordering = ['param_name']


@admin.register(Parameter)
class ParamAdmin(admin.ModelAdmin):
    list_display = ['key', 'value', 'preload', 'description']
    ordering = ['key']
    search_fields = ['key', 'value']


@admin.register(TradePlaceType)
class TradePlaceTypeAdmin(admin.ModelAdmin):
    list_display = ['type_name', 'descr', 'color', 'wall_color', 'roof_color']
    ordering = ['type_name']

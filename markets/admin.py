from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from markets.forms import DmUserCreationForm, DmUserChangeForm
from markets.models import *


class DmUserAdmin(UserAdmin):
    add_form = DmUserCreationForm
    form = DmUserChangeForm
    model = DmUser
    list_display = ("phone", "first_name", "last_name", "email", "is_staff", "is_active",)
    list_filter = ("phone", "first_name", "last_name", "email", "is_staff", "is_active",)
    fieldsets = ((None, {"fields": ("first_name", "last_name", "phone", "password", "email")}), ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}))
    add_fieldsets = ((None, {"fields": ("first_name", "last_name", "phone", "password1", "password2", "email", "is_staff", "is_active", "groups", "user_permissions")}),)
    search_fields = ("phone",)
    ordering = ("phone",)


admin.site.register(DmUser, DmUserAdmin)


@admin.register(Market)
class MarketAdmin(admin.ModelAdmin):
    list_display = ['id', 'market_name', 'additional_name']
    ordering = ['market_name', 'additional_name']


@admin.register(SvgSchema)
class SvgSchemaAdmin(admin.ModelAdmin):
    list_display = ['id', 'market', 'order', 'floor', 'descr']
    list_filter = ['market']
    ordering = ['market', 'order']


@admin.register(MkImage)
class MkImageAdmin(admin.ModelAdmin):
    list_display = ['market', 'image']
    list_filter = ['market']
    ordering = ['market']


@admin.register(GlobalConfig)
class GlobalConfigAdmin(admin.ModelAdmin):
    list_display = ['param_name', 'param_data', 'descr']
    ordering = ['param_name']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['date_transaction', 'user', 'booking_status', 'booking_status_case', 'booking_files', 'renter_id', 'location_number', 'scheme', 'descr']
    list_filter = ['user']
    readonly_fields = ['trade_place']
    ordering = ['user']


@admin.register(Parameter)
class ParamAdmin(admin.ModelAdmin):
    list_display = ['key', 'value', 'preload', 'description']
    ordering = ['key']
    search_fields = ['key', 'value']


@admin.register(RdcError)
class RdcErrorAdmin(admin.ModelAdmin):
    list_display = ['object', 'text', 'created_at']
    list_filter = ['object']


@admin.register(StuffAction)
class StuffActionAdmin(admin.ModelAdmin):
    list_display = ['action', 'description']

    @staticmethod
    def action(action):
        return format_html('<a href="{}">{}</a>', action.link, action.title)


# -------------------------------------------------------------------------------------------------


@admin.register(ContractStatusType)
class ContractStatusTypeAdmin(admin.ModelAdmin):
    list_display = ['type_name', 'descr']
    ordering = ['type_name']


@admin.register(Locality)
class LocalityAdmin(admin.ModelAdmin):
    list_display = ['locality_name', 'locality_type', 'descr', 'parent']
    list_filter = ['parent']
    ordering = ['locality_name']


@admin.register(LocalityType)
class LocalityTypeAdmin(admin.ModelAdmin):
    list_display = ['type_name', 'descr']
    ordering = ['type_name']


@admin.register(MarketFireProtection)
class MarketFireProtectionAdmin(admin.ModelAdmin):
    list_display = ['fp_name', 'descr']
    ordering = ['fp_name']


@admin.register(MarketProfitability)
class MarketFireProtectionAdmin(admin.ModelAdmin):
    list_display = ['profitability_name', 'descr']
    ordering = ['profitability_name']


@admin.register(MarketType)
class MarketTypeAdmin(admin.ModelAdmin):
    list_display = ['type_name', 'descr']
    ordering = ['type_name']


@admin.register(RenterType)
class RenterTypeAdmin(admin.ModelAdmin):
    list_display = ['type_name', 'descr']
    ordering = ['type_name']


@admin.register(StreetType)
class StreetTypeAdmin(admin.ModelAdmin):
    list_display = ['type_name', 'descr']
    ordering = ['type_name']


@admin.register(TradePlaceType)
class TradePlaceTypeAdmin(admin.ModelAdmin):
    list_display = ['type_name', 'descr', 'color', 'wall_color', 'roof_color']
    ordering = ['type_name']


@admin.register(TradeSector)
class TradeSectorAdmin(admin.ModelAdmin):
    list_display = ['sector_name', 'descr']
    ordering = ['sector_name']


@admin.register(TradeSpecType)
class TradeSpecTypeAdmin(admin.ModelAdmin):
    list_display = ['type_name', 'descr', 'color', 'wall_color', 'roof_color']
    ordering = ['type_name']


@admin.register(TradeType)
class TradeTypeAdmin(admin.ModelAdmin):
    list_display = ['type_name', 'type_num', 'descr']
    ordering = ['type_name']

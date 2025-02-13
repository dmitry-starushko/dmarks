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
    list_display = ['id', 'market_name', 'additional_name', 'market_id', 'market_type']
    ordering = ['market_name', 'additional_name']


@admin.register(MarketPhone)
class MarketPhoneAdmin(admin.ModelAdmin):
    list_display = ['phone']
    ordering = ['phone']
    list_filter = ['market']


@admin.register(MarketEmail)
class MarketEmailAdmin(admin.ModelAdmin):
    list_display = ['email']
    ordering = ['email']
    list_filter = ['market']


@admin.register(SvgSchema)
class SvgSchemaAdmin(admin.ModelAdmin):
    list_display = ['id', 'market', 'order', 'floor']
    list_filter = ['market']
    ordering = ['market', 'order']


@admin.register(MkImage)
class MkImageAdmin(admin.ModelAdmin):
    list_display = ['market', 'image']
    list_filter = ['market']
    ordering = ['market']


@admin.register(Parameter)
class ParamAdmin(admin.ModelAdmin):
    list_display = ['key', 'value', 'preload', 'description']
    ordering = ['key']
    search_fields = ['key', 'value']


@admin.register(MarketObservation)
class MarketObservationAdmin(admin.ModelAdmin):
    list_display = ['key', 'decimal']
    list_filter = ['market']
    readonly_fields = ['key', 'market', 'decimal']
    ordering = ['key']
    search_fields = ['key']


@admin.register(GlobalObservation)
class GlobalObservationAdmin(admin.ModelAdmin):
    list_display = ['key', 'decimal']
    ordering = ['key']
    search_fields = ['key']


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
    list_display = ['sector_name', 'descr', 'color', 'wall_color', 'roof_color']
    ordering = ['sector_name']


@admin.register(TradeSpecType)
class TradeSpecTypeAdmin(admin.ModelAdmin):
    list_display = ['type_name', 'descr', 'color', 'wall_color', 'roof_color']
    ordering = ['type_name']


@admin.register(TradeType)
class TradeTypeAdmin(admin.ModelAdmin):
    list_display = ['type_name', 'descr']
    ordering = ['type_name']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'published', 'unpublished', 'calendar_event', 'type', 'text', 'read']
    list_filter = ['user']
    # readonly_fields = ['read', 'attachment', 'question_uuid']
    readonly_fields = ['read', 'attachment']
    ordering = ['-published']


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['title', 'address', 'city', 'district']
    ordering = ['title']


@admin.register(ContactPhone)
class ContactPhoneAdmin(admin.ModelAdmin):
    list_display = ['phone']
    ordering = ['phone']
    list_filter = ['contact']


@admin.register(ContactEmail)
class ContactEmailAdmin(admin.ModelAdmin):
    list_display = ['email']
    ordering = ['email']
    list_filter = ['contact']


@admin.register(LogRecord)
class LogRecordAdmin(admin.ModelAdmin):
    list_display = ['created_at_mt', 'user', 'kind', 'text']
    list_filter = ['user']
    readonly_fields = ['created_at', 'user', 'kind', 'text']
    ordering = ['-created_at']
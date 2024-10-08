# Миксин для корректного определения типа интернет-подключения
from decimal import Decimal
from django.conf import settings


class MkMixin:
    @property
    def mk_sewerage(self):
        return self.infr_sewerage_type if self.infr_sewerage else "отсутствует"

    @property
    def mk_market_name(self):
        return settings.DISP_RE.sub(' ', self.market_name)

    @property
    def mk_additional_name(self):
        return settings.DISP_RE.sub(' ', self.additional_name)

    @property
    def mk_geo_full_address(self):
        return settings.DISP_RE.sub(' ', self.geo_full_address)

    @property
    def mk_full_name(self):
        return f"{self.mk_market_name}, {self.mk_additional_name}"


class TpMixin:
    @property
    def tp_internet_connection(self):
        match self.impr_internet, self.impr_internet_type_id:
            case False, _:
                return "отсутствует"
            case True, 0:
                return "не указано"
            case True, 1:
                return "проводное"
            case True, 2:
                return "беспроводное"
            case _:
                return "ошибка в данных"

    @property
    def tp_power_supply_cost(self):
        return self.pay_electricity if self.impr_electricity else Decimal(0)

    @property
    def tp_internet_cost(self):
        return self.pay_internet if self.impr_internet else Decimal(0)

    @property
    def tp_heat_supply_cost(self):
        return self.pay_heat_supply if self.impr_heat_supply else Decimal(0)

    @property
    def tp_air_conditioning_cost(self):
        return self.pay_air_conditioning if self.impr_air_conditioning else Decimal(0)

    @property
    def tp_plumbing_cost(self):
        return self.pay_plumbing if self.impr_plumbing else Decimal(0)

    @property
    def tp_drains_cost(self):
        return self.pay_drains if self.impr_drains else Decimal(0)

    @property
    def tp_add_equipment_cost(self):
        return self.pay_add_equipment if self.impr_add_equipment else Decimal(0)

    @property
    def tp_fridge_cost(self):
        return self.pay_fridge if self.impr_fridge else Decimal(0)

    @property
    def tp_shopwindows_cost(self):
        return self.pay_shopwindows if self.impr_shopwindows else Decimal(0)

    @property
    def tp_sewerage_cost(self):
        return self.pay_sewerage if self.impr_sewerage else Decimal(0)

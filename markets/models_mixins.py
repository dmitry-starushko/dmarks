# Миксин для корректного определения типа интернет-подключения
from decimal import Decimal


class TpMixin:
    @property
    def internet_connection_type(self):
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
    def cost_power_supply(self):
        return self.pay_electricity if self.impr_electricity else Decimal(0)

    @property
    def cost_internet(self):
        return self.pay_internet if self.impr_internet else Decimal(0)

    @property
    def cost_heat_supply(self):
        return self.pay_heat_supply if self.impr_heat_supply else Decimal(0)

    @property
    def cost_air_conditioning(self):
        return self.pay_air_conditioning if self.impr_air_conditioning else Decimal(0)

    @property
    def cost_plumbing(self):
        return self.pay_plumbing if self.impr_plumbing else Decimal(0)

    @property
    def cost_drains(self):
        return self.pay_drains if self.impr_drains else Decimal(0)

    @property
    def cost_add_equipment(self):
        return self.pay_add_equipment if self.impr_add_equipment else Decimal(0)

    @property
    def cost_fridge(self):
        return self.pay_fridge if self.impr_fridge else Decimal(0)

    @property
    def cost_shopwindows(self):
        return self.pay_shopwindows if self.impr_shopwindows else Decimal(0)

    @property
    def cost_sewerage(self):
        return self.pay_sewerage if self.impr_sewerage else Decimal(0)

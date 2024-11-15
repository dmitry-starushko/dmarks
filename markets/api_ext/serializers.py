from rest_framework.serializers import ModelSerializer, IntegerField
from markets.models import TradePlace, TradePlaceType, TradeSpecType, TradeType


class TradePlaceTypeSerializer(ModelSerializer):
    class Meta:
        model = TradePlaceType
        fields = ['type_name']


class TradeSpecTypeSerializer(ModelSerializer):
    class Meta:
        model = TradeSpecType
        fields = ['type_name']


class TradeTypeSerializer(ModelSerializer):
    class Meta:
        model = TradeType
        fields = ['type_name', 'type_num']


class TradePlaceSerializer(ModelSerializer):
    trade_type = TradeTypeSerializer(many=False, read_only=True)
    trade_place_type = TradePlaceTypeSerializer(many=False, read_only=True)
    trade_spec_type_id_act = TradeSpecTypeSerializer(many=False, read_only=True)
    trade_spec_type_id_rec = TradeSpecTypeSerializer(many=False, read_only=True)

    class Meta:
        model = TradePlace
        fields = [
            'meas_area',
            'meas_length',
            'meas_height',
            'meas_width',
            'impr_electricity',
            'impr_heat_supply',
            'impr_air_conditioning',
            'impr_plumbing',
            'impr_sewerage',
            'impr_drains',
            'impr_internet',
            'impr_internet_type_id',
            'impr_add_equipment',
            'impr_fridge',
            'impr_shopwindow',
            'price',
            'street_vending',
            'contract_rent',
            'receiv_state',
            'receiv_amount',
            'pay_electricity',
            'pay_heat_supply',
            'pay_air_conditioning',
            'pay_plumbing',
            'pay_sewerage',
            'pay_drains',
            'pay_internet',
            'pay_add_equipment',
            'pay_fridge',
            'pay_shopwindows',
            'location_sector',
            'location_row',
            'location_floor',
            'location_number',
            'renter',
            'additional',
            'internal_id',
            'speciality_recommend',
            'speciality_actual',
            'activities_type',
            'trade_type',
            'trade_place_type',
            'trade_spec_type_id_act',
            'trade_spec_type_id_rec',
        ]


class TradePlaceSerializerO(TradePlaceSerializer):
    legend_id = IntegerField(source='trade_place_type_id')

    class Meta:
        model = TradePlace
        fields = TradePlaceSerializer.Meta.fields + ['legend_id']


class TradePlaceSerializerS(TradePlaceSerializer):
    legend_id = IntegerField(source='trade_spec_type_id_act_id')

    class Meta:
        model = TradePlace
        fields = TradePlaceSerializer.Meta.fields + ['legend_id']





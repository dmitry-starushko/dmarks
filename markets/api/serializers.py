from rest_framework.serializers import ModelSerializer, IntegerField
from markets.models import Market, TradePlace, TradePlaceType, SvgSchema, TradeSpecType, TradeSector


class MarketSerializer(ModelSerializer):
    class Meta:
        model = Market


class TradePlaceTypeSerializer(ModelSerializer):
    class Meta:
        model = TradePlaceType
        fields = ['id', 'type_name', 'color', 'wall_color', 'roof_color', 'wall_color_css', 'roof_color_css']


class TradeSpecTypeSerializer(ModelSerializer):
    class Meta:
        model = TradeSpecType
        fields = ['id', 'type_name', 'color', 'wall_color', 'roof_color', 'wall_color_css', 'roof_color_css']


class TradeSectorSerializer(ModelSerializer):
    class Meta:
        model = TradeSector
        fields = ['id', 'sector_name', 'color', 'wall_color', 'roof_color', 'wall_color_css', 'roof_color_css']


class TradePlaceSerializer(ModelSerializer):
    trade_place_type = TradePlaceTypeSerializer(many=False, read_only=True)
    trade_spec_type_id_act = TradeSpecTypeSerializer(many=False, read_only=True)

    class Meta:
        model = TradePlace
        fields = ['id', 'location_number', 'price', 'trade_place_type', 'trade_spec_type_id_act']


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


class TradePlaceSerializerSec(TradePlaceSerializer):
    legend_id = IntegerField(source='location_sector_id')

    class Meta:
        model = TradePlace
        fields = TradePlaceSerializer.Meta.fields + ['legend_id']


class SchemeSerializer(ModelSerializer):
    class Meta:
        model = SvgSchema
        fields = ['id', 'floor', 'order', 'descr']





from rest_framework.serializers import ModelSerializer
from markets.models import Market, TradePlace, TradePlaceType, SvgSchema, TradeSpecType, TradeSector


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


class SchemeSerializer(ModelSerializer):
    class Meta:
        model = SvgSchema
        fields = ['id', 'floor', 'order', 'descr']





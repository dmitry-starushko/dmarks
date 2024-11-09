from rest_framework.serializers import ModelSerializer
from markets.models import Market, TradePlace, TradePlaceType, SvgSchema


class MarketSerializer(ModelSerializer):
    class Meta:
        model = Market


class TradePlaceTypeSerializer(ModelSerializer):
    class Meta:
        model = TradePlaceType
        fields = ["id", "type_name", "color", "wall_color_css", "roof_color_css"]


class TradePlaceSerializer(ModelSerializer):
    trade_place_type = TradePlaceTypeSerializer(many=False, read_only=True)

    class Meta:
        model = TradePlace
        fields = ["id", "location_number", "tp_actual_specialization", "price", "trade_place_type"]


class SchemeSerializer(ModelSerializer):
    class Meta:
        model = SvgSchema
        fields = ["id", "floor", "order", "descr"]





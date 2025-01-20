from rest_framework.serializers import ModelSerializer
from markets.models import TradePlaceType, TradeSpecType, TradeSector


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





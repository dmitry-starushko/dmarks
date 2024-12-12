from markets.models import Market, TradePlace


def apply_filter(query, filter_name: str, filter_body: str):
    return query


def filter_markets(text: str):
    return (Market.objects.filter(market_name__icontains=text) |
            Market.objects.filter(additional_name__icontains=text) |
            Market.objects.filter(geo_city__locality_name__icontains=text) |
            Market.objects.filter(geo_district__locality_name__icontains=text)).order_by('geo_city__locality_name', 'geo_district__locality_name', 'market_name', 'additional_name')


def filter_outlets(filters):
    return TradePlace.objects.select_related('market', 'trade_place_type', 'trade_spec_type_id_act', 'market__geo_city', 'market__geo_district')

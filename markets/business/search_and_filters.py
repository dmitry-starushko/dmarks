from markets.models import Market, TradePlace


def filter_markets(text: str):
    return (Market.objects.filter(market_name__icontains=text) |
            Market.objects.filter(additional_name__icontains=text) |
            Market.objects.filter(geo_city__locality_name__icontains=text) |
            Market.objects.filter(geo_district__locality_name__icontains=text)).order_by('geo_city__locality_name', 'geo_district__locality_name', 'market_name', 'additional_name')


def filter_outlets(filters):
    query = TradePlace.objects.filter(scheme__isnull=False)
    for kind, value in filters.items():
        match kind, value:
            case 'markets', [*market_pks]:
                query = query.filter(market_id__in=market_pks)
            case 'specializations', [*type_pks]:
                query = query.filter(trade_spec_type_id_act_id__in=type_pks)
            case 'occupation-types', [*type_pks]:
                query = query.filter(trade_place_type_id__in=type_pks)
            case 'facilities', {**facilities}:
                query = query.filter(**facilities)
            case 'price-range', {'min': p_min, 'max': p_max}:
                query = query.filter(price__gte=p_min, price__lte=p_max)
            case 'area-range', {'min': a_min, 'max': a_max}:
                query = query.filter(meas_area__gte=a_min, meas_area__lte=a_max)
            case 'outlet-number', o_num:
                query = query.filter(location_number__icontains=o_num)
    return query

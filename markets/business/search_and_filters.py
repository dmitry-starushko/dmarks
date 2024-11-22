from markets.models import Market


def apply_filter(query, filter_name: str, filter_body: str):
    return query


def filter_markets(text: str):
    # return Market.objects.filter(market_name__icontains=text)
    return Market.objects.filter(geo_district__isnull=True)

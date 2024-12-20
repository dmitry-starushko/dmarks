from django.db import transaction
from markets.enums import LocationType
from markets.models import Locality, LocalityType, Market, MarketType, MarketProfitability, MarketFireProtection, StreetType, Validators


def create_market(market_id: str, data):
    match data:
        case {
            'market_name': str(market_name),
            'additional_name': str(additional_name),
            'market_type': str(market_type),
            'branch': str(branch),
            'profitability': str(profitability),
            'infr': {
                'fire_protection': str(infr_fire_protection),
                'parking': int(infr_parking),
                'entrance': int(infr_entrance),
                'restroom': int(infr_restroom),
                'storage': int(infr_storage),
                'water_pipes': bool(infr_water_pipes),
                'sewerage': bool(infr_sewerage),
                'sewerage_type': str(infr_sewerage_type)
            },
            'geo': {
                'lat': float(lat),
                'lng': float(lng),
                'city': str(geo_city),
                'district': str(geo_district),
                'street': str(geo_street),
                'street_type': str(geo_street_type),
                'house': str(geo_house),
                'index': str(geo_index)
            },
            'market_area': float(market_area),
            'schedule': str(schedule),
            'ads': str(ads)
        } if infr_parking >= 0 and infr_entrance >= 0 and infr_restroom >= 0 and infr_storage >= 0 and market_area >= 0.0 and -90.0 <= lat <= 90.0 and -180.0 <= lng <= 180.0:
            Validators.market_id(market_id)
            Validators.postal_code(geo_index)
            with transaction.atomic():
                city_type, _ = LocalityType.objects.get_or_create(type_name=LocationType.CITY)
                district_type, _ = LocalityType.objects.get_or_create(type_name=LocationType.DISTRICT)
                city, _ = Locality.objects.get_or_create(locality_name=geo_city, defaults={'parent_id': Locality.default_pk(), 'locality_type': city_type})
                district, _ = Locality.objects.get_or_create(parent=city, locality_name=geo_district, defaults={'locality_type': district_type})
                Market.objects.create(
                    market_id=market_id,
                    market_name=market_name,
                    additional_name=additional_name,
                    market_type=MarketType.objects.get_or_create(type_name=market_type)[0],
                    branch=branch,
                    profitability=MarketProfitability.objects.get_or_create(profitability_name=profitability)[0],
                    infr_fire_protection=MarketFireProtection.objects.get_or_create(fp_name=infr_fire_protection)[0],
                    infr_parking=infr_parking,
                    infr_entrance=infr_entrance,
                    infr_restroom=infr_restroom,
                    infr_storage=infr_storage,
                    infr_water_pipes=infr_water_pipes,
                    infr_sewerage=infr_sewerage,
                    infr_sewerage_type=infr_sewerage_type,
                    lat=lat,
                    lng=lng,
                    geo_city=city,
                    geo_district=district,
                    geo_street_type=StreetType.objects.get_or_create(type_name=geo_street_type)[0],
                    geo_street=geo_street,
                    geo_house=geo_house,
                    geo_index=geo_index,
                    market_area=market_area,
                    schedule=schedule,
                    ads=ads,
                )
            return True
        case _:
            raise ValueError(data)

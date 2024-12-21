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
            'market_area': float(market_area),
            'schedule': str(schedule),
            'ads': str(ads),
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
            }
        } if infr_parking >= 0 \
             and infr_entrance >= 0 \
             and infr_restroom >= 0 \
             and infr_storage >= 0 \
             and market_area >= 0.0 \
             and -90.0 <= lat <= 90.0 \
             and -180.0 <= lng <= 180.0:
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
                    ads=ads)
            return True
        case _: raise ValueError(data)


def get_market(market_id: str):
    market = Market.objects.get(market_id=market_id)
    return {
            'market_id': market.market_id,
            'market_name': market.market_name,
            'additional_name': market.additional_name,
            'market_type': f'{market.market_type}',
            'branch': market.branch,
            'profitability': f'{market.profitability}',
            'market_area': market.market_area,
            'schedule': market.schedule,
            'ads': market.ads,
            'infr': {
                'fire_protection': f'{market.infr_fire_protection}',
                'parking': market.infr_parking,
                'entrance': market.infr_entrance,
                'restroom': market.infr_restroom,
                'storage': market.infr_storage,
                'water_pipes': market.infr_water_pipes,
                'sewerage': market.infr_sewerage,
                'sewerage_type': market.infr_sewerage_type
            },
            'geo': {
                'lat': market.lat,
                'lng': market.lng,
                'city': f'{market.geo_city}',
                'district': f'{market.geo_district}',
                'street': market.geo_street,
                'street_type': f'{market.geo_street_type}',
                'house': market.geo_house,
                'index': market.geo_index
            }
        }


def update_market(market_id: str, data):
    market = Market.objects.get(market_id=market_id)
    with transaction.atomic():
        for key, value in data.items():
            match key, value:
                case 'market_name', str(market_name): market.market_name = market_name
                case 'additional_name', str(additional_name): market.additional_name = additional_name
                case 'market_type', str(market_type): market.market_type = MarketType.objects.get_or_create(type_name=market_type)[0]
                case 'branch', str(branch): market.branch = branch
                case 'profitability', str(profitability): market.profitability = MarketProfitability.objects.get_or_create(profitability_name=profitability)[0]
                case 'market_area', float(market_area) if market_area >= 0.0: market.market_area = market_area
                case 'schedule', str(schedule): market.schedule = schedule
                case 'ads', str(ads): market.ads = ads
                case 'infr', {**infr}:
                    for i_key, i_value in infr.items():
                        match i_key, i_value:
                            case 'fire_protection', str(infr_fire_protection): market.infr_fire_protection = MarketFireProtection.objects.get_or_create(fp_name=infr_fire_protection)[0]
                            case 'parking', int(infr_parking) if infr_parking >= 0: market.infr_parking = infr_parking
                            case 'entrance', int(infr_entrance) if infr_entrance >= 0: market.infr_entrance = infr_entrance
                            case 'restroom', int(infr_restroom) if infr_restroom >= 0: market.infr_restroom = infr_restroom
                            case 'storage', int(infr_storage) if infr_storage >= 0: market.infr_storage = infr_storage
                            case 'water_pipes', bool(infr_water_pipes): market.infr_water_pipes = infr_water_pipes
                            case 'sewerage', bool(infr_sewerage): market.infr_sewerage = infr_sewerage
                            case 'sewerage_type', str(infr_sewerage_type): market.infr_sewerage_type = infr_sewerage_type
                            case _: raise ValueError((i_key, i_value))
                case 'geo', {**geo}:
                    match geo:
                        case {'city': str(geo_city), 'district': str(geo_district)}:
                            city_type, _ = LocalityType.objects.get_or_create(type_name=LocationType.CITY)
                            district_type, _ = LocalityType.objects.get_or_create(type_name=LocationType.DISTRICT)
                            city, _ = Locality.objects.get_or_create(locality_name=geo_city, defaults={'parent_id': Locality.default_pk(), 'locality_type': city_type})
                            district, _ = Locality.objects.get_or_create(parent=city, locality_name=geo_district, defaults={'locality_type': district_type})
                            market.geo_city = city
                            market.geo_district = district
                        case {'city': c}: raise ValueError(c)
                        case {'district': d}: raise ValueError(d)
                        case _: pass
                    for g_key, g_value in geo.items():
                        match g_key, g_value:
                            case 'lat', float(lat) if -90.0 <= lat <= 90.0: market.lat = lat
                            case 'lng', float(lng) if -180.0 <= lng <= 180.0: market.lng = lng
                            case 'street', str(geo_street): market.geo_street = geo_street
                            case 'street_type', str(geo_street_type): market.geo_street = StreetType.objects.get_or_create(type_name=geo_street_type)[0]
                            case 'house', str(geo_house): market.geo_house = geo_house
                            case 'index', str(geo_index):
                                Validators.postal_code(geo_index)
                                market.geo_index = geo_index
                            case 'city', _: pass
                            case 'district', _: pass
                            case _: raise ValueError((g_key, g_value))

                case _: raise ValueError((key, value))
        market.save()
        return True


def delete_market(market_id: str):
    Market.objects.get(market_id=market_id).delete()
    return True


# --- Outlets ---


def create_market_outlets(market_id: str, data):
    market = Market.objects.get(market_id=market_id)
    with transaction.atomic():
        for olt in data:
            match olt:
                case {

                }: pass
                case _: raise ValueError(olt)
        return True


def get_market_outlets(market_id: str):
    market = Market.objects.get(market_id=market_id)
    return False


def update_market_outlets(market_id: str, data):
    market = Market.objects.get(market_id=market_id)
    return False


def delete_market_outlets(market_id: str, data):
    market = Market.objects.get(market_id=market_id)
    return False


# --- Schemes ---


def create_market_schemes(market_id: str, data):
    # Not implemented for current iteration
    return False


def get_market_schemes(market_id: str):
    # Not implemented for current iteration
    return False


def update_market_schemes(market_id: str, data):
    # Not implemented for current iteration
    return False


def delete_market_schemes(market_id: str, data):
    # Not implemented for current iteration
    return False


# --- Images ---


def create_market_images(market_id: str, data):
    market = Market.objects.get(market_id=market_id)
    return False


def get_market_images(market_id: str):
    market = Market.objects.get(market_id=market_id)
    return False


def update_market_images(market_id: str, data):
    market = Market.objects.get(market_id=market_id)
    return False


def delete_market_images(market_id: str, data):
    market = Market.objects.get(market_id=market_id)
    return False


# --- Phones ---


def create_market_phones(market_id: str, data):
    market = Market.objects.get(market_id=market_id)
    return False


def get_market_phones(market_id: str):
    market = Market.objects.get(market_id=market_id)
    return False


def update_market_phones(market_id: str, data):
    market = Market.objects.get(market_id=market_id)
    return False


def delete_market_phones(market_id: str, data):
    market = Market.objects.get(market_id=market_id)
    return False


# --- Emails ---


def create_market_emails(market_id: str, data):
    market = Market.objects.get(market_id=market_id)
    return False


def get_market_emails(market_id: str):
    market = Market.objects.get(market_id=market_id)
    return False


def update_market_emails(market_id: str, data):
    market = Market.objects.get(market_id=market_id)
    return False


def delete_market_emails(market_id: str, data):
    market = Market.objects.get(market_id=market_id)
    return False
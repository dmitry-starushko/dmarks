from django.db import transaction
from markets.enums import LocationType, OutletState
from markets.models import Locality, LocalityType, Market, MarketType, MarketProfitability, MarketFireProtection, StreetType, TradeType, TradePlaceType, TradeSpecType, TradeSector, DmUser, \
    Notification, File
from markets.validators import Validators
import base64


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
                            case 'street_type', str(geo_street_type): market.geo_street_type = StreetType.objects.get_or_create(type_name=geo_street_type)[0]
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
                    'location_number': str(location_number),
                    'location_row': str(location_row),
                    'price': float(price),
                    'street_vending': bool(street_vending),
                    'trade_type': str(trade_type),
                    'trade_place_type': str(trade_place_type),
                    'trade_spec_type_id_act': str(trade_spec_type_id_act),
                    'trade_spec_type_id_rec': str(trade_spec_type_id_rec),
                    'location_sector': str(location_sector),
                    'meas': {
                        'area': float(meas_area),
                        'length': float(meas_length),
                        'height': float(meas_height),
                        'width': float(meas_width)
                    },
                    'impr': {
                        'electricity': bool(impr_electricity),
                        'heat_supply': bool(impr_heat_supply),
                        'air_conditioning': bool(impr_air_conditioning),
                        'plumbing': bool(impr_plumbing),
                        'sewerage': bool(impr_sewerage),
                        'drains': bool(impr_drains),
                        'internet': bool(impr_internet),
                        'internet_type_id': int(impr_internet_type_id),
                        'add_equipment': bool(impr_add_equipment),
                        'fridge': bool(impr_fridge),
                        'shopwindow': bool(impr_shopwindow)
                    }
                } if price >= 0.0 \
                     and meas_width >= 0.0 \
                     and meas_height >= 0.0 \
                     and meas_length >= 0.0 \
                     and meas_area >= 0.0 \
                     and 0 <= impr_internet_type_id <= 2 \
                     and trade_place_type in OutletState \
                     and location_number.startswith(market_id):
                    Validators.outlet_number(location_number)
                    market.trade_places.create(
                        location_number=location_number,
                        location_row=location_row,
                        price=price,
                        street_vending=street_vending,
                        trade_type=TradeType.objects.get_or_create(type_name=trade_type)[0],
                        trade_place_type=TradePlaceType.objects.get_or_create(type_name=trade_place_type)[0],
                        trade_spec_type_id_act=TradeSpecType.objects.get_or_create(type_name=trade_spec_type_id_act)[0],
                        trade_spec_type_id_rec=TradeSpecType.objects.get_or_create(type_name=trade_spec_type_id_rec)[0],
                        location_sector=TradeSector.objects.get_or_create(sector_name=location_sector)[0],
                        meas_area=meas_area,
                        meas_length=meas_length,
                        meas_height=meas_height,
                        meas_width=meas_width,
                        impr_electricity=impr_electricity,
                        impr_heat_supply=impr_heat_supply,
                        impr_air_conditioning=impr_air_conditioning,
                        impr_plumbing=impr_plumbing,
                        impr_sewerage=impr_sewerage,
                        impr_drains=impr_drains,
                        impr_internet=impr_internet,
                        impr_internet_type_id=impr_internet_type_id,
                        impr_add_equipment=impr_add_equipment,
                        impr_fridge=impr_fridge,
                        impr_shopwindow=impr_shopwindow
                    )
                case _: raise ValueError(olt)
        return True


def get_market_outlets(market_id: str):
    market = Market.objects.get(market_id=market_id)
    return [{
        'location_number': olt.location_number,
        'location_row': olt.location_row,
        'price': olt.price,
        'street_vending': olt.street_vending,
        'trade_type': f'{olt.trade_type}',
        'trade_place_type': f'{olt.trade_place_type.type_name}',
        'trade_spec_type_id_act': f'{olt.trade_spec_type_id_act}',
        'trade_spec_type_id_rec': f'{olt.trade_spec_type_id_rec}',
        'location_sector': f'{olt.location_sector}',
        'meas': {
            'area': olt.meas_area,
            'length': olt.meas_length,
            'height': olt.meas_height,
            'width': olt.meas_width
        },
        'impr': {
            'electricity': olt.impr_electricity,
            'heat_supply': olt.impr_heat_supply,
            'air_conditioning': olt.impr_air_conditioning,
            'plumbing': olt.impr_plumbing,
            'sewerage': olt.impr_sewerage,
            'drains': olt.impr_drains,
            'internet': olt.impr_internet,
            'internet_type_id': olt.impr_internet_type_id,
            'add_equipment': olt.impr_add_equipment,
            'fridge':olt.impr_fridge,
            'shopwindow': olt.impr_shopwindow
        }
    } for olt in market.trade_places.select_related('trade_type', 'trade_place_type', 'trade_spec_type_id_act', 'trade_spec_type_id_rec', 'location_sector')]


def update_market_outlets(market_id: str, data):
    market = Market.objects.get(market_id=market_id)
    with transaction.atomic():
        for olt in data:
            if 'location_number' in olt:
                r = market.trade_places.get(location_number=olt['location_number'])
                for key, value in olt.items():
                    match key, value:
                        case 'location_number', _: pass
                        case 'location_row', str(location_row): r.location_row = location_row
                        case 'price', float(price) if price >= 0.0: r.price = price
                        case 'street_vending', bool(street_vending): r.street_vending = street_vending
                        case 'trade_type', str(trade_type): r.trade_type = TradeType.objects.get_or_create(type_name=trade_type)[0]
                        case 'trade_place_type', str(trade_place_type) if trade_place_type in OutletState:
                            match r.rented_by, trade_place_type:
                                case None, _: r.trade_place_type = TradePlaceType.objects.get_or_create(type_name=trade_place_type)[0]
                                case _, OutletState.RENTED: r.trade_place_type = TradePlaceType.objects.get_or_create(type_name=OutletState.RENTED)[0]
                                case _: raise ValueError(f'Статус ТМ {r.location_number} не может быть изменен на {trade_place_type}: ТМ арендовано')
                        case 'trade_spec_type_id_act', str(trade_spec_type_id_act): r.trade_spec_type_id_act = TradeSpecType.objects.get_or_create(type_name=trade_spec_type_id_act)[0]
                        case 'trade_spec_type_id_rec', str(trade_spec_type_id_rec): r.trade_spec_type_id_rec = TradeSpecType.objects.get_or_create(type_name=trade_spec_type_id_rec)[0]
                        case 'location_sector', str(location_sector): r.location_sector = TradeSector.objects.get_or_create(sector_name=location_sector)[0]
                        case 'meas', {**meas}:
                            for m_key, m_value in meas.items():
                                match m_key, m_value:
                                    case 'area', float(meas_area) if meas_area >= 0.0: r.meas_area = meas_area
                                    case 'length', float(meas_length) if meas_length >= 0.0: r.meas_length = meas_length
                                    case 'height', float(meas_height) if meas_height >= 0.0: r.meas_height = meas_height
                                    case 'width', float(meas_width) if meas_width >= 0.0: r.meas_width = meas_width
                                    case _: raise ValueError((m_key, m_value))
                        case 'impr', {**impr}:
                            for i_key, i_value in impr.items():
                                match i_key, i_value:
                                    case 'electricity', bool(impr_electricity): r.impr_electricity = impr_electricity
                                    case 'heat_supply', bool(impr_heat_supply): r.impr_heat_supply = impr_heat_supply
                                    case 'air_conditioning', bool(impr_air_conditioning): r.impr_air_conditioning = impr_air_conditioning
                                    case 'plumbing', bool(impr_plumbing): r.impr_plumbing = impr_plumbing
                                    case 'sewerage', bool(impr_sewerage): r.impr_sewerage = impr_sewerage
                                    case 'drains', bool(impr_drains): r.impr_drains = impr_drains
                                    case 'internet', bool(impr_internet): r.impr_internet = impr_internet
                                    case 'internet_type_id', int(impr_internet_type_id) if 0 <= impr_internet_type_id <= 2: r.impr_internet_type_id = impr_internet_type_id
                                    case 'add_equipment', bool(impr_add_equipment): r.impr_add_equipment = impr_add_equipment
                                    case 'fridge', bool(impr_fridge): r.impr_fridge = impr_fridge
                                    case 'shopwindow', bool(impr_shopwindow): r.impr_shopwindow = impr_shopwindow
                                    case _: raise ValueError((i_key, i_value))
                        case _: raise ValueError((key, value))
                r.save()
            else:
                raise ValueError(olt)
    return True


def delete_market_outlets(market_id: str, data):
    market = Market.objects.get(market_id=market_id)
    with transaction.atomic():
        for number in data:
            market.trade_places.get(location_number=number).delete()
    return True


# --- Schemes ---


def create_market_schemes(market_id: str, data):
    # Not implemented for current iteration
    market = Market.objects.get(market_id=market_id)
    return False


def get_market_schemes(market_id: str):
    # Not implemented for current iteration
    market = Market.objects.get(market_id=market_id)
    return False


def update_market_schemes(market_id: str, data):
    # Not implemented for current iteration
    market = Market.objects.get(market_id=market_id)
    return False


def delete_market_schemes(market_id: str, data):
    # Not implemented for current iteration
    market = Market.objects.get(market_id=market_id)
    return False


# --- Images ---


def create_market_images(market_id: str, data):
    # Not implemented for current iteration
    market = Market.objects.get(market_id=market_id)
    return False


def get_market_images(market_id: str):
    # Not implemented for current iteration
    market = Market.objects.get(market_id=market_id)
    return False


def update_market_images(market_id: str, data):
    # Not implemented for current iteration
    market = Market.objects.get(market_id=market_id)
    return False


def delete_market_images(market_id: str, data):
    # Not implemented for current iteration
    market = Market.objects.get(market_id=market_id)
    return False


# --- Phones ---


def create_market_phones(market_id: str, data):
    # Not implemented for current iteration
    market = Market.objects.get(market_id=market_id)
    return False


def get_market_phones(market_id: str):
    # Not implemented for current iteration
    market = Market.objects.get(market_id=market_id)
    return False


def update_market_phones(market_id: str, data):
    # Not implemented for current iteration
    market = Market.objects.get(market_id=market_id)
    return False


def delete_market_phones(market_id: str, data):
    # Not implemented for current iteration
    market = Market.objects.get(market_id=market_id)
    return False


# --- Emails ---


def create_market_emails(market_id: str, data):
    # Not implemented for current iteration
    market = Market.objects.get(market_id=market_id)
    return False


def get_market_emails(market_id: str):
    # Not implemented for current iteration
    market = Market.objects.get(market_id=market_id)
    return False


def update_market_emails(market_id: str, data):
    # Not implemented for current iteration
    market = Market.objects.get(market_id=market_id)
    return False


def delete_market_emails(market_id: str, data):
    # Not implemented for current iteration
    market = Market.objects.get(market_id=market_id)
    return False


# --- Notifications ---

def create_notifications(itn: str | None, data):
    user = DmUser.objects.get(aux_data__itn=itn) if itn is not None else None
    result = []
    with transaction.atomic():
        for ntf in data:
            args = {
                'user': user,
                'read': False
            }
            match ntf:
                case {**items}:
                    for key, value in items.items():
                        match key, value:
                            case 'published', str(_): args |= {key: value}
                            case 'unpublished', str(_): args |= {key: value}
                            case 'calendar_event', bool(_): args |= {key: value}
                            case 'question_uuid', str(_): args |= {key: value}
                            case 'type', str(_): args |= {key: value}
                            case 'text', str(_): args |= {key: value}
                            case 'attachment', {  # -- Не описывать в документации к данной итерации --
                                'file_name': str(file_name),
                                'file_content': str(file_content)
                            }: args |= {'attachment': File.objects.create(file_name=file_name, file_content=base64.b64decode(file_content.encode('ascii')))}
                            case _: raise ValueError((key, value))
                    result.append(Notification.objects.create(**args).id)
                case _: raise ValueError(ntf)
        return result


def get_notifications(itn: str | None):
    user = DmUser.objects.get(aux_data__itn=itn) if itn is not None else None
    query = user.notifications.all() if user is not None else Notification.objects.filter(user__isnull=True)
    return [{
        'id': ntf.id,
        'published': f'{ntf.published}',
        'unpublished':  f'{ntf.unpublished}',
        'calendar_event':  ntf.calendar_event,
        'type': ntf.type,
        'text': ntf.text,
        # 'has-attachment': ntf.attachment is not None,
        'read':  ntf.read
    } for ntf in query]


def delete_notifications(itn: str | None, data):
    user = DmUser.objects.get(aux_data__itn=itn) if itn is not None else None
    manager = user.notifications if user is not None else Notification.objects
    with transaction.atomic():
        for npk in data:
            manager.get(pk=npk).delete()
    return True

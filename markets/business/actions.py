import datetime
from xml.etree import ElementTree as Et
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Max, Min
from markets.enums import Observation, LogRecordKind, OutletState
from markets.decorators import globally_lonely_action
from markets.models import TradePlace, SvgSchema, RdcError, Market, GlobalObservation, Notification, LogRecord, TradePlaceType
from markets.validators import Validators

try:  # To avoid deploy problems
    from transmutation import Svg3DTM
except ModuleNotFoundError:
    class Svg3DTM:
        pass


@globally_lonely_action(None)
def restore_db_consistency():
    with transaction.atomic():
        errors = dict()
        svg3dtm = Svg3DTM()

        # -- Clear outlet's location floor
        print(f'Подготовка к обработке...')
        TradePlace.objects.update(scheme=None)

        # -- Set outlet's location floors
        for sch in SvgSchema.objects.all():
            print(f'Обрабатывается {sch}')
            sch_title = str(sch)
            errors[sch_title] = (err_list := [])
            try:
                tree = Et.fromstring(sch.svg_schema)
            except Et.ParseError:
                err_list += ['Ошибка парсинга SVG']
                continue
            try:
                svg3dtm.transmutate(sch.svg_schema)
            except Exception as e:
                err_list += [f'Не удалось построить 3D модель: {e}']
            tit = tree.iter()
            for node in tit:
                if node.tag.endswith('path') and 'class' in node.attrib and node.attrib['class'] == 'outlet':
                    if 'id' in node.attrib:
                        path_id = node.attrib['id']
                        try:
                            Validators.outlet_number(path_id)
                        except ValidationError:
                            err_list += [f'Номер ТМ в SVG не соответствует формату: <{path_id}>']
                        try:
                            tp = TradePlace.objects.get(location_number=path_id)
                        except TradePlace.DoesNotExist:
                            err_list += [f'ТМ <{path_id}> не найдено в БД']
                        else:
                            if sch.market_id != tp.market_id:
                                err_list += [f'ТМ #{tp.id} <{path_id}> относится к другому рынку "{tp.market}"']
                            elif tp.scheme is not None:
                                err_list += [f'ТМ #{tp.id} <{path_id}> уже помечено как относящееся к уровню #{tp.scheme}']
                            else:
                                tp.scheme = sch
                                tp.save()
                    else:
                        err_list += [f'Номер ТМ не указан в SVG']
        for tp in TradePlace.objects.all():
            print(f'Обрабатывается {tp}')
            if tp.rented_by is None and tp.trade_place_type.type_name == OutletState.RENTED:
                tp.trade_place_type = TradePlaceType.objects.get_or_create(type_name=OutletState.UNKNOWN)[0]
                tp.save()
            errors[f'{tp}'] = (err_list := [])
            if tp.scheme_id is None:
                err_list += [f'ТМ не привязано к схеме: scheme_id = {tp.scheme_id}']

        RdcError.objects.all().delete()
        for key, value in errors.items():
            for err in value:
                RdcError.objects.create(object=key, text=err)


@globally_lonely_action(None)
def logrotate():
    today = datetime.datetime.today()
    for kind in LogRecordKind:
        try:
            ttl = settings.LOG_TTL_DAYS[kind]
        except KeyError:
            ttl = settings.LOG_TTL_DAYS_DEFAULT
        LogRecord.objects.filter(created_at__lt=today-datetime.timedelta(days=ttl)).delete()


@globally_lonely_action(None)
def delete_obsolete_notifications():
    today = datetime.datetime.today()
    Notification.objects.filter(unpublished__lt=today, read=True, calendar_event=False).delete()


@globally_lonely_action(None)
def observe_all():
    for market in Market.objects.all():
        # -- Renting cost limits --
        r, _ = market.observations.get_or_create(key=Observation.OUTLET_RENTING_COST_MIN)
        r.decimal = market.trade_places.aggregate(Min('price', default=0))['price__min']
        r.save()
        r, _ = market.observations.get_or_create(key=Observation.OUTLET_RENTING_COST_MAX)
        r.decimal = market.trade_places.aggregate(Max('price', default=0))['price__max']
        r.save()
        # -- Area limits --
        r, _ = market.observations.get_or_create(key=Observation.OUTLET_AREA_MIN)
        r.decimal = market.trade_places.aggregate(Min('meas_area', default=0))['meas_area__min']
        r.save()
        r, _ = market.observations.get_or_create(key=Observation.OUTLET_AREA_MAX)
        r.decimal = market.trade_places.aggregate(Max('meas_area', default=0))['meas_area__max']
        r.save()
    # -- Renting cost limits --
    r, _ = GlobalObservation.objects.get_or_create(key=Observation.OUTLET_RENTING_COST_MIN)
    r.decimal = TradePlace.objects.aggregate(Min('price', default=0))['price__min']
    r.save()
    r, _ = GlobalObservation.objects.get_or_create(key=Observation.OUTLET_RENTING_COST_MAX)
    r.decimal = TradePlace.objects.aggregate(Max('price', default=0))['price__max']
    r.save()
    # -- Area limits --
    r, _ = GlobalObservation.objects.get_or_create(key=Observation.OUTLET_AREA_MIN)
    r.decimal = TradePlace.objects.aggregate(Min('meas_area', default=0))['meas_area__min']
    r.save()
    r, _ = GlobalObservation.objects.get_or_create(key=Observation.OUTLET_AREA_MAX)
    r.decimal = TradePlace.objects.aggregate(Max('meas_area', default=0))['meas_area__max']
    r.save()

from xml.etree import ElementTree as Et
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Max, Min
from markets.enums import Observation
from markets.decorators import globally_lonely_action
from markets.models import TradePlace, SvgSchema, Validators, RdcError, Market, GlobalObservation

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
                        tps = [tp for tp in TradePlace.objects.filter(location_number=path_id)]
                        if not tps:
                            err_list += [f'ТМ <{path_id}> не найдено в БД']
                        elif len(tps) > 1:
                            tp_ids = ', '.join([f'#{tp.id}' for tp in tps])
                            err_list += [f'В БД имеется более одного ТМ с номером <{path_id}>: {tp_ids}']
                        else:
                            tp = tps[0]
                            if sch.market_id != tp.market_id:
                                err_list += [f'ТМ #{tp.id} <{path_id}> относится к другому рынку "{tp.market}"']
                            elif tp.scheme is not None:
                                err_list += [f'ТМ #{tp.id} <{path_id}> уже помечено как относящееся к уровню #{tp.scheme}']
                            else:
                                tp.scheme = sch
                                tp.save()
                    else:
                        err_list += [f'Номер ТМ не указан в SVG']
        tps = [tp for tp in TradePlace.objects.all()]
        for tp in tps:
            print(f'Обрабатывается {tp}')
            errors[f'{tp}'] = (err_list := [])
            if tp.scheme_id is None:
                err_list += [f'ТМ не привязано к схеме: scheme_id = {tp.scheme_id}']
            try:
                Validators.outlet_number(tp.location_number)
            except ValidationError:
                err_list += [f'Номер ТМ не соответствует формату: <{tp.location_number}>']

        RdcError.objects.all().delete()
        for key, value in errors.items():
            for err in value:
                RdcError.objects.create(object=key, text=err)


@globally_lonely_action(None)
def observe_all():
    # 1. -- Renting cost limits -----------------
    for market in Market.objects.all():
        r, _ = market.observations.get_or_create(key=Observation.OUTLET_RENTING_COST_MIN)
        r.decimal = market.trade_places.aggregate(Min('price', default=0))['price__min']
        r.save()
        r, _ = market.observations.get_or_create(key=Observation.OUTLET_RENTING_COST_MAX)
        r.decimal = market.trade_places.aggregate(Max('price', default=0))['price__max']
        r.save()
    r, _ = GlobalObservation.objects.get_or_create(key=Observation.OUTLET_RENTING_COST_MIN)
    r.decimal = TradePlace.objects.aggregate(Min('price', default=0))['price__min']
    r.save()
    r, _ = GlobalObservation.objects.get_or_create(key=Observation.OUTLET_RENTING_COST_MAX)
    r.decimal = TradePlace.objects.aggregate(Max('price', default=0))['price__max']
    r.save()

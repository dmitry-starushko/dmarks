from django.db import transaction
from markets.decorators import globally_lonely_action
from markets.models import TradePlace, SvgSchema, RdcError
from xml.etree import ElementTree as ET


@globally_lonely_action
def restore_db_consistency():
    with transaction.atomic():
        errors = dict()

        # -- Clear outlet's location floor
        print(f'Подготовка к согласованию...')
        TradePlace.objects.update(location_floor=None)

        # -- Set outlet's location floors
        for sch in SvgSchema.objects.all():
            print(f'Обрабатывается {sch}')
            sch_title = str(sch)
            errors[sch_title] = (err_list := [])
            try:
                tree = ET.fromstring(sch.svg_schema)
            except ET.ParseError:
                err_list += ['Ошибка парсинга SVG']
                continue
            tit = tree.iter()
            for node in tit:
                if node.tag.endswith('path') and 'class' in node.attrib and node.attrib['class'] == 'outlet':
                    if 'id' in node.attrib:
                        pid = node.attrib['id']
                        tps = [tp for tp in TradePlace.objects.filter(location_number=pid)]
                        if not tps:
                            err_list += [f'ТМ <{pid}> не найдено в БД']
                        elif len(tps) > 1:
                            tp_ids = ', '.join([f'#{tp.id}' for tp in tps])
                            err_list += [f'В БД имеется более одного ТМ с номером <{pid}>: {tp_ids}']
                        else:
                            tp = tps[0]
                            if sch.market_id != tp.market_id:
                                err_list += [f'ТМ #{tp.id} <{pid}> относится к рынку "{tp.market}"']
                            elif tp.location_floor:
                                err_list += [f'ТМ #{tp.id} <{pid}> уже помечено как относящееся к уровню #{tp.location_floor}']
                            else:
                                tp.location_floor = sch.id
                                tp.save()
                    else:
                        err_list += [f'Номер ТМ не указан в SVG']

        tps = [tp for tp in TradePlace.objects.filter(location_floor=None)]
        tp_ids = ', '.join([f'#{tp.id} <{tp.location_number}>' for tp in tps])
        errors["ТМ без привязки к схеме"] = [tp_ids]

        RdcError.objects.all().delete()
        for key, value in errors.items():
            for err in value:
                RdcError.objects.create(object=key, text=err)

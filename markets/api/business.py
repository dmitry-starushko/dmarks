from threading import Lock

from django.conf import settings
from django.db import transaction
from redis import Redis

from markets.models import TradePlace, SvgSchema, RdcError
from xml.etree import ElementTree as ET


redis = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
rdc_lock = Lock()
rdc_action = 'actions:running:restoredbconsistency'


def rdc_is_running():
    return redis.exists(rdc_action)


def restore_db_consistency():
    if rdc_is_running():
        return
    try:
        redis.set(name=rdc_action, value=1, ex=3600)  # TODO exp. time to settings
        with rdc_lock:
            with transaction.atomic():
                errors = dict()

                # -- Clear outlet's location floor
                print(f'Подготовка...')
                for tp in TradePlace.objects.all():
                    tp.location_floor = None
                    tp.save()

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
                                    if tp.location_floor:
                                        err_list += [f'ТМ с номером <{pid}> уже помечено как относящееся к уровню #{tp.location_floor}']
                                    else:
                                        tp.location_floor = sch.id
                                        tp.save()
                            else:
                                err_list += [f'Номер торгового места не указан в SVG']

                tps = [tp for tp in TradePlace.objects.filter(location_floor=None)]
                tp_ids = ', '.join([f'#{tp.id} <{tp.location_number}>' for tp in tps])
                errors["ТМ без привязки к схеме"] = [tp_ids]

                RdcError.objects.all().delete()
                for key, value in errors.items():
                    for err in value:
                        RdcError.objects.create(object=key, text=err)
    finally:
        redis.delete(rdc_action)

from drf_spectacular.utils import inline_serializer
from rest_framework import fields


def preprocessing_filter_spec(endpoints):
    filtered = []
    for (path, path_regex, method, callback) in endpoints:
        if path.startswith("/extapi/"):
            filtered.append((path, path_regex, method, callback))
    return filtered


def oapi_result(result, suffix: str = ''):
    return inline_serializer(f'Result{suffix}', {'result': result})


def oapi_market_serializer(create: bool, suffix: str = ''):
    return inline_serializer(f'Market_description{suffix}', {
                'market_name': fields.CharField(required=create, help_text='Название рынка'),
                'additional_name': fields.CharField(required=create, help_text='Дополнительное название рынка'),
                'market_type': fields.CharField(required=create, help_text='Тип рынка (по справочнику)'),
                'branch': fields.CharField(required=create, help_text='Отделение'),
                'profitability': fields.CharField(required=create, help_text='Категория рентабельности рынка (по справочнику)'),
                'market_area': fields.FloatField(required=create, help_text='Площадь рынка'),
                'schedule': fields.CharField(required=create, help_text='График работы рынка, текст с разметкой markdown'),
                'ads': fields.CharField(required=create, help_text='Рекламный текст, с разметкой markdown'),
                'infr': inline_serializer(f'Equipment{suffix}', {
                    'fire_protection': fields.CharField(required=create, help_text='Тип противопожарной защиты (по справочнику)'),  # str(infr_fire_protection),
                    'parking': fields.IntegerField(required=create, help_text='Количество парковок'),  # int(infr_parking),
                    'entrance': fields.IntegerField(required=create, help_text='Количество подъездов'),  # int(infr_entrance),
                    'restroom': fields.IntegerField(required=create, help_text='Количество санузлов'),  # int(infr_restroom),
                    'storage':  fields.IntegerField(required=create, help_text='Количество складских помещений'),  # int(infr_storage),
                    'water_pipes': fields.BooleanField(required=create, help_text='Наличие водопровода'),  # bool(infr_water_pipes),
                    'sewerage': fields.BooleanField(required=create, help_text='Наличие канализации'),  # bool(infr_sewerage),
                    'sewerage_type': fields.CharField(required=create, help_text='Тип канализации'),  # str(infr_sewerage_type)
                }, required=create),
                'geo': inline_serializer(f'Location{suffix}', {
                    'lat': fields.FloatField(required=create, help_text='Географическая широта'),  # float(lat),
                    'lng': fields.FloatField(required=create, help_text='Географическая долгота'),  # float(lng),
                    'city': fields.CharField(required=create, help_text='Город (по справочнику)'),  # str(geo_city),
                    'district': fields.CharField(required=create, help_text='Район города (по справочнику)'),  # str(geo_district),
                    'street': fields.CharField(required=create, help_text='Улица'),  # str(geo_street),
                    'street_type': fields.CharField(required=create, help_text='Тип улицы (по справочнику)'),  # str(geo_street_type),
                    'house': fields.CharField(required=create, help_text='Номер дома'),  # str(geo_house),
                    'index': fields.CharField(required=create, help_text='Почтовый индекс'),  # str(geo_index)
                }, required=create)
            })

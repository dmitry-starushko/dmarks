from drf_spectacular.utils import inline_serializer
from rest_framework import fields


def preprocessing_filter_spec(endpoints):
    filtered = []
    for (path, path_regex, method, callback) in endpoints:
        if path.startswith('/extapi/'):
            filtered.append((path, path_regex, method, callback))
    return filtered


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
            'fire_protection': fields.CharField(required=create, help_text='Тип противопожарной защиты (по справочнику)'),
            'parking': fields.IntegerField(required=create, help_text='Количество парковок'),
            'entrance': fields.IntegerField(required=create, help_text='Количество подъездов'),
            'restroom': fields.IntegerField(required=create, help_text='Количество санузлов'),
            'storage': fields.IntegerField(required=create, help_text='Количество складских помещений'),
            'water_pipes': fields.BooleanField(required=create, help_text='Наличие водопровода'),
            'sewerage': fields.BooleanField(required=create, help_text='Наличие канализации'),
            'sewerage_type': fields.CharField(required=create, help_text='Тип канализации'),
        }, required=create),
        'geo': inline_serializer(f'Location{suffix}', {
            'lat': fields.FloatField(required=create, help_text='Географическая широта'),
            'lng': fields.FloatField(required=create, help_text='Географическая долгота'),
            'city': fields.CharField(required=create, help_text='Город (по справочнику)'),
            'district': fields.CharField(required=create, help_text='Район города (по справочнику)'),
            'street': fields.CharField(required=create, help_text='Улица'),
            'street_type': fields.CharField(required=create, help_text='Тип улицы (по справочнику)'),
            'house': fields.CharField(required=create, help_text='Номер дома'),
            'index': fields.CharField(required=create, help_text='Почтовый индекс'),
        }, required=create)
    })


def oapi_outlet_serializer(create: bool, suffix: str = ''):
    return inline_serializer(f'Outlet_description{suffix}', {
        'location_number': fields.CharField(required=True, help_text='Номер торгового места'),
        'location_row': fields.CharField(required=create, help_text='Ряд'),
        'price': fields.FloatField(required=create, help_text='Стоимость аренды'),
        'street_vending': fields.BooleanField(required=create, help_text='Возможность выносной торговли'),
        'trade_type': fields.CharField(required=create, help_text='Тип (по справочнику)'),
        'trade_place_type': fields.CharField(required=create, help_text='Занятость (по справочнику)'),
        'trade_spec_type_id_act': fields.CharField(required=create, help_text='Специализация (по справочнику)'),
        'trade_spec_type_id_rec': fields.CharField(required=create, help_text='Рекомендованная специализация (по справочнику)'),
        'location_sector': fields.CharField(required=create, help_text='Сектор (по справочнику)'),
        'meas': inline_serializer(f'Dimensions{suffix}', {
            'area': fields.FloatField(required=create, help_text='Площадь'),
            'length': fields.FloatField(required=create, help_text='Длина'),
            'width': fields.FloatField(required=create, help_text='Ширина'),
            'height': fields.FloatField(required=create, help_text='Высота'),
        }),
        'impr': inline_serializer(f'Impr{suffix}', {
            'electricity': fields.BooleanField(required=create, help_text='Наличие электричества'),
            'heat_supply': fields.BooleanField(required=create, help_text='Наличие теплоснабжения'),
            'air_conditioning': fields.BooleanField(required=create, help_text='Наличие кондиционирования'),
            'plumbing': fields.BooleanField(required=create, help_text='Наличие водопровода'),
            'sewerage': fields.BooleanField(required=create, help_text='Наличие канализации'),
            'drains': fields.BooleanField(required=create, help_text='Наличие стоков'),
            'internet': fields.BooleanField(required=create, help_text='Наличие подключения к Internet'),
            'internet_type_id': fields.IntegerField(required=create, help_text='Тип подключения к Internet'),
            'add_equipment': fields.BooleanField(required=create, help_text='Наличие дополнительного оборудования'),
            'fridge': fields.BooleanField(required=create, help_text='Наличие морозильных установок'),
            'shopwindow': fields.BooleanField(required=create, help_text='Наличие витрин'),
        })
    }, many=True)


def oapi_notification_serializer(create: bool, suffix: str = ''):
    return inline_serializer(f'Notification_description{suffix}', {
        'published': fields.CharField(required=True, help_text='Дата публикации в формате YYYY-MM-DD'),
        'unpublished': fields.CharField(required=True, help_text='Дата снятия с публикации в формате YYYY-MM-DD'),
        'calendar_event': fields.BooleanField(required=True, help_text='Флаг календарного события. Если true, уведомление отображается в Календаре Личного Кабинета'),
        'question_uuid': fields.UUIDField(required=False, allow_null=False, help_text='UUID вопроса. Если указан, пользователь может ответить Да/Нет на уведомление, см. Спецификации API РД'),
        'type': fields.CharField(required=True, help_text='Тип уведомления: info | warn | alrt'),
        'text': fields.CharField(required=True, help_text='Текст уведомления с разметкой markdown'),
    } | ({} if create else {
        'read': fields.BooleanField(required=True, help_text='Признак прочтения уведомления'),
    }), many=True)


def oapi_result(result, suffix: str = ''):
    return inline_serializer(f'Result{suffix}', {'result': result})

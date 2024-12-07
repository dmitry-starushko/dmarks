from decimal import Decimal
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.conf import settings
from django.db.models import Index


class Validators:
    @staticmethod
    def _rxv(rx: str, msg: str):
        return RegexValidator(regex=rx, message=msg)

    @staticmethod
    def css_color(value):
        return Validators._rxv('^#[\\da-fA-F]{6}$', "Ожидается значение в формате #ffffff")(value)

    @staticmethod
    def hex(value):
        return Validators._rxv('^0x[\\da-fA-F]{1,6}$', "Ожидается значение в формате 0xffffff")(value)

    @staticmethod
    def outlet_number(value):
        return Validators._rxv('^\\d{9}[а-яё]{0,1}$', "Ожидается значение в формате 999999999[a]")(value)

    @staticmethod
    def market_id(value):
        return Validators._rxv('^\\d{3}$', "Ожидается значение в формате 999")(value)

    @staticmethod
    def itn(value):
        return Validators._rxv('^((?:\\d{10})|(?:\\d{12}))$', "Ожидается значение в формате 999")(value)


class DbItem(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract: bool = True


# -- DmUser ---------------------------------------------------------------------------------------


class DmUserManager(BaseUserManager):
    def create_user(self, phone, password, email, **extra_fields):
        if not phone:
            raise ValueError('Телефон должен быть указан')
        email = self.normalize_email(email)
        user = self.model(phone=phone, email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone, password, email, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Суперпользователь должен иметь is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Суперпользователь должен иметь is_superuser=True.")
        return self.create_user(phone, password, email, **extra_fields)


class DmUser(AbstractUser):
    username = None
    phone = models.CharField(unique=True, max_length=16, null=False, blank=False)
    email = models.EmailField(unique=True, max_length=255)
    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ["first_name", "last_name", "email"]
    objects = DmUserManager()

    def __str__(self):
        return self.email


class File(DbItem):
    file_name = models.CharField(max_length=512)  # -- имя файла --
    file_content = models.BinaryField()  # -- двоичный образ файла --

    class Meta:
        verbose_name = "Файл"
        verbose_name_plural = "Файлы"

    def __str__(self):
        return f'Файл {self.file_name}'


class AuxUserData(DbItem):
    user = models.OneToOneField(DmUser, on_delete=models.CASCADE, related_name='aux_data')  # -- ассоциированный пользователь --
    confirmed = models.BooleanField(default=False)  # -- данные подтверждены администрацией --
    itn = models.CharField(max_length=12, validators=[Validators.itn])  # -- ИНН --
    usr_le_extract = models.OneToOneField(File, related_name='usr_le_extract', on_delete=models.SET_NULL, null=True)  # -- выписка из ЕСГРЮЛ, Unified State Register of Legal Entities --
    passport_image = models.OneToOneField(File, related_name='passport_image', on_delete=models.SET_NULL, null=True)  # -- скан паспорта --

    class Meta:
        verbose_name = "Доп. данные"
        verbose_name_plural = "Доп. данные"

    def __str__(self):
        return f'Данные "{self.user}"'


# -- Legacy data ----------------------------------------------------------------------------------


class LocalityType(models.Model):
    type_name = models.CharField(unique=True, db_comment='Наименование типа')
    descr = models.TextField(blank=True, null=True, db_comment='Описание')

    @classmethod
    def default_pk(cls):
        item, _ = cls.objects.get_or_create(type_name="Не указано")
        return item.pk

    class Meta:
        managed = True
        ordering = ['type_name']
        db_table = 'locality_type'
        db_table_comment = 'Типы населенных пунктов'
        verbose_name = "Тип локации"
        verbose_name_plural = "Типы локаций"

    def __str__(self):
        return f'{self.type_name}'


class Locality(models.Model):
    locality_name = models.CharField(db_comment='Наименование населенного пункта')
    locality_type = models.ForeignKey(LocalityType, models.SET_DEFAULT, default=LocalityType.default_pk, db_comment='Тип населенного пункта')
    parent = models.ForeignKey('self', models.SET_NULL, blank=True, null=True, db_comment='Родительская запись. Иерархическое подчинение')
    descr = models.TextField(blank=True, null=True, db_comment='Описание')

    @classmethod
    def default_pk(cls):
        item, _ = cls.objects.get_or_create(locality_name="Не указано")
        return item.pk

    class Meta:
        managed = True
        ordering = ['locality_name']
        db_table = 'locality'
        db_table_comment = 'Населенные пункты'
        verbose_name = "Локация"
        verbose_name_plural = "Локации"

    def __str__(self):
        return f'{self.locality_name}'


class MarketFireProtection(models.Model):
    fp_name = models.CharField(unique=True, db_comment='Наименование противопожарной системы')
    descr = models.TextField(blank=True, null=True, db_comment='Описание')

    @classmethod
    def default_pk(cls):
        item, _ = cls.objects.get_or_create(fp_name="Не указано")
        return item.pk

    class Meta:
        managed = True
        ordering = ['fp_name']
        db_table = 'market_fire_protection'
        db_table_comment = 'Наличие и состав противопожарных систем'
        verbose_name = "Тип противопожарной системы"
        verbose_name_plural = "Типы противопожарных систем"

    def __str__(self):
        return f'{self.fp_name}'


class MarketProfitability(models.Model):
    profitability_name = models.CharField(unique=True, db_comment='Наименование категории рентабельности рынка')
    descr = models.TextField(blank=True, null=True, db_comment='Описание')

    @classmethod
    def default_pk(cls):
        item, _ = cls.objects.get_or_create(profitability_name="Не указано")
        return item.pk

    class Meta:
        managed = True
        ordering = ['profitability_name']
        db_table = 'market_profitability'
        db_table_comment = 'Категория рентабельности рынка'
        verbose_name = "Категория рентабельности рынка"
        verbose_name_plural = "Категории рентабельности рынка"

    def __str__(self):
        return f'{self.profitability_name}'


class MarketType(models.Model):
    type_name = models.CharField(unique=True, db_comment='Наименование типа рынка')
    descr = models.TextField(blank=True, null=True, db_comment='Описание')

    @classmethod
    def default_pk(cls):
        item, _ = cls.objects.get_or_create(type_name="Не указано")
        return item.pk

    class Meta:
        managed = True
        ordering = ['type_name']
        db_table = 'market_type'
        db_table_comment = 'Типы рынков'
        verbose_name = "Тип рынка"
        verbose_name_plural = "Типы рынка"

    def __str__(self):
        return f'{self.type_name}'


class StreetType(models.Model):
    type_name = models.CharField(unique=True, db_comment='Наименование типа улиц (сокращенное)')
    descr = models.TextField(blank=True, null=True, db_comment='Описание (полное наименование)')

    @classmethod
    def default_pk(cls):
        item, _ = cls.objects.get_or_create(type_name="Не указано")
        return item.pk

    class Meta:
        managed = True
        ordering = ['type_name']
        db_table = 'street_type'
        db_table_comment = 'Типы улиц'
        verbose_name = "Тип улицы"
        verbose_name_plural = "Типы улиц"

    def __str__(self):
        return f'{self.type_name}'


class TradePlaceType(models.Model):
    type_name = models.CharField(unique=True, db_comment='Наименование типа занятости торгового места')
    color = models.CharField(max_length=7, default='#ffffff', validators=[Validators.css_color], db_comment='Цвет в формате #ffffff')
    wall_color = models.CharField(max_length=8, default='0xffffff', validators=[Validators.hex], db_comment='Цвет стен ТМ в формате 0xffffff, для 3D')
    roof_color = models.CharField(max_length=8, default='0xffffff', validators=[Validators.hex], db_comment='Цвет крыш ТМ в формате 0xffffff, для 3D')
    descr = models.TextField(blank=True, null=True, db_comment='Опиcание')

    @classmethod
    def default_pk(cls):
        item, _ = cls.objects.get_or_create(type_name="Не указано")
        return item.pk

    class Meta:
        managed = True
        ordering = ['type_name']
        db_table = 'trade_place_type'
        db_table_comment = 'Типы занятости торгового места'
        verbose_name = "Тип занятости ТМ"
        verbose_name_plural = "Типы занятости ТМ"

    def __str__(self):
        return f'{self.type_name}'

    @property
    def wall_color_css(self):
        return f'#{hex(int(self.wall_color, 16))[2:]}'

    @property
    def roof_color_css(self):
        return f'#{hex(int(self.roof_color, 16))[2:]}'


class TradeSector(models.Model):
    sector_name = models.CharField(unique=True, db_comment='Наименование сектора рынка')
    color = models.CharField(max_length=7, default='#ffffff', validators=[Validators.css_color], db_comment='Цвет в формате #ffffff')
    wall_color = models.CharField(max_length=8, default='0xffffff', validators=[Validators.hex], db_comment='Цвет стен ТМ в формате 0xffffff, для 3D')
    roof_color = models.CharField(max_length=8, default='0xffffff', validators=[Validators.hex], db_comment='Цвет крыш ТМ в формате 0xffffff, для 3D')
    descr = models.TextField(blank=True, null=True, db_comment='Описание')

    @classmethod
    def default_pk(cls):
        item, _ = cls.objects.get_or_create(sector_name="Не указано")
        return item.pk

    class Meta:
        managed = True
        ordering = ['sector_name']
        db_table = 'trade_sector'
        db_table_comment = 'Сектора рынков'
        verbose_name = "Сектор"
        verbose_name_plural = "Секторы"

    def __str__(self):
        return f'{self.sector_name}'

    @property
    def wall_color_css(self):
        return f'#{hex(int(self.wall_color, 16))[2:]}'

    @property
    def roof_color_css(self):
        return f'#{hex(int(self.roof_color, 16))[2:]}'


class TradeSpecType(models.Model):
    type_name = models.CharField(unique=True, db_comment='Наименование типа специализации торгового места')
    color = models.CharField(max_length=7, default='#ffffff', validators=[Validators.css_color], db_comment='Цвет в формате #ffffff')
    wall_color = models.CharField(max_length=8, default='0xffffff', validators=[Validators.hex], db_comment='Цвет стен ТМ в формате 0xffffff, для 3D')
    roof_color = models.CharField(max_length=8, default='0xffffff', validators=[Validators.hex], db_comment='Цвет крыш ТМ в формате 0xffffff, для 3D')
    descr = models.TextField(blank=True, null=True, db_comment='Описание')

    @classmethod
    def default_pk(cls):
        item, _ = cls.objects.get_or_create(type_name="Не указано")
        return item.pk

    class Meta:
        managed = True
        ordering = ['type_name']
        db_table = 'trade_spec_type'
        db_table_comment = 'Типы специализации торгового места'
        verbose_name = "Тип специализации ТМ"
        verbose_name_plural = "Типы специализации ТМ"

    def __str__(self):
        return f'{self.type_name}'

    @property
    def wall_color_css(self):
        return f'#{hex(int(self.wall_color, 16))[2:]}'

    @property
    def roof_color_css(self):
        return f'#{hex(int(self.roof_color, 16))[2:]}'


class TradeType(models.Model):
    type_name = models.CharField(unique=True, db_comment='Наименование типа торгового места')
    type_num = models.SmallIntegerField(unique=True, default=0, db_comment='Код типа объекта')
    descr = models.TextField(blank=True, null=True, db_comment='Описание')

    @classmethod
    def default_pk(cls):
        item, _ = cls.objects.get_or_create(type_name="Не указано")
        return item.pk

    class Meta:
        managed = True
        ordering = ['type_name']
        db_table = 'trade_type'
        db_table_comment = 'Типы торгового места'
        verbose_name = "Тип ТМ"
        verbose_name_plural = "Типы ТМ"

    def __str__(self):
        return f'{self.type_name}'


class Market(models.Model):
    market_id = models.CharField(max_length=3, unique=True, validators=[Validators.outlet_number], db_comment='Уникальный идентификатор рынка')
    market_name = models.CharField(max_length=1000, db_comment='Наименование рынка')
    additional_name = models.CharField(max_length=1000, db_comment='Дополнительное наименование')
    market_type = models.ForeignKey(MarketType, models.SET_DEFAULT, default=MarketType.default_pk, db_comment='id - тип рынка')

    profitability = models.ForeignKey(MarketProfitability, models.SET_DEFAULT, default=MarketProfitability.default_pk, db_comment='id - категория рентабельности')
    infr_fire_protection = models.ForeignKey(MarketFireProtection, models.SET_DEFAULT, default=MarketFireProtection.default_pk, db_comment='id - противопожарные системы')
    infr_parking = models.SmallIntegerField(default=0, db_comment='Кол-во парковок')
    infr_entrance = models.SmallIntegerField(default=0, db_comment='Кол-во подъездов')
    infr_restroom = models.SmallIntegerField(default=0, db_comment='Кол-во санузлов')
    infr_water_pipes = models.BooleanField(default=False, db_comment='Наличие водопровода')
    infr_sewerage = models.BooleanField(default=False, db_comment='Наличие канализации')
    infr_sewerage_type = models.CharField(max_length=1000, default='Не указано', db_comment='Тип канализации')
    infr_storage = models.SmallIntegerField(default=0, db_comment='Кол-во складских помещений')

    lat = models.FloatField(default=0.0, db_comment='Широта - координата рынка')
    lng = models.FloatField(default=0.0, db_comment='Долгота - координата рынка')
    geo_city = models.ForeignKey(Locality, models.SET_DEFAULT, default=Locality.default_pk, db_comment='Город - id')
    geo_district = models.ForeignKey(Locality, models.SET_DEFAULT, default=Locality.default_pk, related_name='markets_geo_district_set', db_comment='Район - id')
    geo_street_type = models.ForeignKey(StreetType, models.SET_DEFAULT, default=StreetType.default_pk, db_comment='Тип улицы - id')
    geo_street = models.TextField(default='Не указано', db_comment='Наименование улицы')
    geo_house = models.CharField(max_length=50, default='Не указано', db_comment='Дом')
    geo_index = models.CharField(max_length=10, default='Не указано', db_comment='Индекс')
    geo_full_address = models.CharField(default='Не указано', db_comment='Полный адрес через запятую')
    market_square = models.FloatField(default=0.0, db_comment='Общая площадь рынка')

    schedule = models.TextField(default='Не указано', db_column='shedule', db_comment='График работы')
    ads = models.TextField(default='Не указано', db_comment='Реклама')
    images: models.QuerySet

    class Meta:
        managed = True
        ordering = ['market_name', 'additional_name']
        db_table = 'markets'
        db_table_comment = 'Информация о рынках'
        verbose_name = "Рынок"
        verbose_name_plural = "Рынки"

    def __str__(self):
        return f'{self.market_name}:{self.additional_name}'

    @property
    def image(self):
        first_img = self.images.first()
        return first_img.image if first_img else settings.DEF_MK_IMG

    @property
    def mk_sewerage(self):
        return self.infr_sewerage_type if self.infr_sewerage else "отсутствует"

    @property
    def mk_water_supply(self):
        return "есть" if self.infr_water_pipes else "отсутствует"

    @property
    def mk_market_name(self):
        return settings.DISP_RE.sub(' ', self.market_name).strip()

    @property
    def mk_additional_name(self):
        return settings.DISP_RE.sub(' ', self.additional_name).strip()

    @property
    def mk_geo_full_address(self):
        return settings.DISP_RE.sub(' ', self.geo_full_address).strip()

    @property
    def mk_geo_index(self):
        return settings.DISP_RE.sub(' ', self.geo_index).strip()

    @property
    def mk_full_name(self):
        return f"{self.mk_market_name}, {self.mk_additional_name}"

    @property
    def mk_full_address(self):
        return f"{self.mk_geo_index}, {self.mk_geo_full_address}"


class SvgSchema(models.Model):
    market = models.ForeignKey(Market, on_delete=models.CASCADE, related_name="schemes", db_comment='id рынка')
    floor = models.CharField(default='Не указано', db_comment='Этаж схемы объекта')
    order = models.IntegerField(default=0, db_comment='Поле для упорядочивания схем')
    svg_schema = models.TextField(default='', db_comment='svg объекта')

    class Meta:
        managed = True
        ordering = ['order']
        db_table = 'svg_schema'
        verbose_name = "Схема"
        verbose_name_plural = "Схемы"

    def __str__(self):
        return f'Схема #{self.id}, уровень "{self.floor}", рынок "{self.market}"'


class TradePlace(models.Model):
    market = models.ForeignKey(Market, models.CASCADE, related_name="trade_places", db_comment='Уникальный идентификатор рынка\r\n')
    trade_type = models.ForeignKey(TradeType, models.SET_DEFAULT, default=TradeType.default_pk, db_comment='Тип торгового места')
    trade_place_type = models.ForeignKey(TradePlaceType, models.SET_DEFAULT, default=TradePlaceType.default_pk, db_comment='Занятость торгового места')
    trade_spec_type_id_act = models.ForeignKey(TradeSpecType, models.SET_DEFAULT, default=TradeSpecType.default_pk, db_column='trade_spec_type_id_act', related_name='tradeplace_trade_spec_type_id_act_set', db_comment='Специализация торгового места (фактическая)')
    trade_spec_type_id_rec = models.ForeignKey(TradeSpecType, models.SET_DEFAULT, default=TradeSpecType.default_pk, db_column='trade_spec_type_id_rec', db_comment='Специализация торгового места (рекомендованная)')
    location_sector = models.ForeignKey(TradeSector, models.SET_DEFAULT, default=TradeSector.default_pk, db_comment='id сектор торгового места')
    scheme = models.ForeignKey(SvgSchema, related_name="outlets", on_delete=models.SET_NULL, null=True)

    location_number = models.CharField(unique=True, validators=[Validators.outlet_number], db_comment='Номер торгового места')
    location_row = models.CharField(default='Не указано', db_comment='Ряд торгового места')

    meas_area = models.FloatField(default=0.0, db_comment='Площадь места')
    meas_length = models.FloatField(default=0.0, db_comment='Длина места')
    meas_height = models.FloatField(default=0.0, db_comment='Высота места')
    meas_width = models.FloatField(default=0.0, db_comment='Ширина места')

    street_vending = models.BooleanField(default=False, db_comment='Возможность выносной торговли')
    impr_electricity = models.BooleanField(default=False, db_comment='Наличие электричества')
    impr_heat_supply = models.BooleanField(default=False, db_comment='Наличие теплоснабжения')
    impr_air_conditioning = models.BooleanField(default=False, db_comment='Наличие кондиционирования')
    impr_plumbing = models.BooleanField(default=False, db_comment='Наличие водопровода')
    impr_sewerage = models.BooleanField(default=False, db_comment='Наличие канализации')
    impr_drains = models.BooleanField(default=False, db_comment='Наличие стоков')
    impr_internet = models.BooleanField(default=False, db_comment='Подключение к сети интернет')
    impr_internet_type_id = models.SmallIntegerField(default=0, db_comment='Тип подключения к сети интернет (0 - не заполнено, 1 - проводной, 2 - беспроводной)')
    impr_add_equipment = models.BooleanField(default=False, db_comment='Наличие стендов, мебели')
    impr_fridge = models.BooleanField(default=False, db_comment='Наличие холодильных установок')
    impr_shopwindow = models.BooleanField(default=False, db_comment='Наличие витрин')
    price = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal(0.0), db_comment='Стоимость аренды торгового места в месяц')

    class Meta:
        managed = True
        ordering = ['location_number']
        db_table = 'trade_place'
        db_table_comment = 'Торговые места'
        indexes = [Index(fields=["location_number"], name='index_by_number')]
        verbose_name = "Торговое место"
        verbose_name_plural = "Торговые места"

    def __str__(self):
        return f'ТМ #{self.id} <{self.location_number}>'

    @property
    def tp_internet_connection(self):
        match self.impr_internet, self.impr_internet_type_id:
            case False, _:
                return "отсутствует"
            case True, 0:
                return "не указано"
            case True, 1:
                return "проводное"
            case True, 2:
                return "беспроводное"
            case _:
                return "ошибка в данных"


class Booking(DbItem):
    outlet = models.ForeignKey(TradePlace, on_delete=models.CASCADE, related_name="bookings", db_comment='Идентификатор торгового места')
    booked_by = models.ForeignKey(DmUser, on_delete=models.CASCADE, related_name="bookings", db_comment='Кто забронировал')

    class Meta:
        managed = True
        ordering = ['-created_at']
        verbose_name = "Бронирование ТМ"
        verbose_name_plural = "Бронирования ТМ"

    def __str__(self):
        return f'Бронирование {self.id}'


# -- NG Data --------------------------------------------------------------------------------------

class MkImage(DbItem):  # -- Market images
    image = models.ImageField(upload_to='markets/%Y/%m/%d')  # картинка
    market = models.ForeignKey(Market, related_name="images", on_delete=models.CASCADE)  # рынок

    class Meta:
        verbose_name = "Изображение"
        verbose_name_plural = "Изображения"

    def __str__(self):
        return f'Фотография рынка #{self.market.id}'


class MarketPhone(DbItem):  # -- Market phones
    phone = models.CharField(unique=True, max_length=16)
    market = models.ForeignKey(Market, related_name="phones", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Телефон"
        verbose_name_plural = "Телефоны"

    def __str__(self):
        return f'{self.phone}'


class MarketEmail(DbItem):  # -- Market phones
    email = models.EmailField(unique=True, max_length=255)
    market = models.ForeignKey(Market, related_name="emails", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "EMail"
        verbose_name_plural = "EMail"

    def __str__(self):
        return f'{self.email}'


class Parameter(DbItem):  # -- NG Parameters
    key = models.CharField(primary_key=True, max_length=50)  # -- ключ --
    value = models.CharField(max_length=250)  # -- значение --
    preload = models.BooleanField(default=False)  # -- используется в контексте --
    description = models.TextField(null=True, blank=True)  # -- описание --

    def __str__(self):
        return f'Параметр "{self.key}"'

    class Meta:
        verbose_name = "Параметр"
        verbose_name_plural = "Параметры"

    @staticmethod
    def value_of(key, default=""):
        try:
            return Parameter.objects.get(pk=key).value
        except Parameter.DoesNotExist:
            return default

    @staticmethod
    def from_value_of(key, constructor, default):
        try:
            return constructor(Parameter.objects.get(pk=key).value)
        except (ValueError, Parameter.DoesNotExist):
            return default


class MarketObservation(DbItem):
    key = models.CharField(max_length=50)  # -- ключ --
    market = models.ForeignKey(Market, related_name="observations", on_delete=models.CASCADE)
    decimal = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal(0.0))

    class Meta:
        verbose_name = "Значение"
        verbose_name_plural = "Значения"
        constraints = [models.UniqueConstraint(fields=["key", "market_id"], name="unique_key_per_market")]

    def __str__(self):
        return f'{self.key}'


class GlobalObservation(DbItem):
    key = models.CharField(unique=True, max_length=50)  # -- ключ --
    decimal = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal(0.0))

    class Meta:
        verbose_name = "Значение"
        verbose_name_plural = "Значения"

    def __str__(self):
        return f'{self.key}'


class RdcError(DbItem):  # -- Errors detected by Restore Database Consistency procedure
    object = models.CharField(max_length=250)  # -- источник --
    text = models.TextField()  # -- проблема --

    class Meta:
        verbose_name = "Ошибка"
        verbose_name_plural = "Ошибки"

    def __str__(self):
        return f'Ошибка "{self.id}"'


class StuffAction(DbItem):  # -- Stuff actions in admin panel
    title = models.CharField(max_length=64)  # -- название --
    link = models.URLField(max_length=512, default="")  # -- ссылка --
    description = models.TextField(null=True, blank=True)  # -- описание --

    class Meta:
        ordering = ["title"]
        verbose_name = "Операция"
        verbose_name_plural = "Операции"

    def __str__(self):
        return f'{self.title}'

# -- May be useful - do not kill! -----------------------------------------------------------------


# class RenterType(models.Model):
#     type_name = models.CharField(unique=True, db_comment='Наименование типа арендатора')
#     descr = models.TextField(blank=True, null=True, db_comment='Описание')
#
#     @classmethod
#     def default_pk(cls):
#         item, _ = cls.objects.get_or_create(type_name="Не указано")
#         return item.pk
#
#     class Meta:
#         managed = True
#         ordering = ['type_name']
#         db_table = 'renter_type'
#         db_table_comment = 'Тип арендатора'
#         verbose_name = "Тип арендатора"
#         verbose_name_plural = "Типы арендаторов"
#
#     def __str__(self):
#         return f'{self.type_name}'
#
#
# class Renter(models.Model):
#     renter_name = models.CharField(db_comment='Наименование арендатора')
#     legal_doc_info = models.CharField(blank=True, null=True, db_comment='Информация об уставных документах')
#     legal_doc_files = models.JSONField(blank=True, null=True, db_comment='Уставные документы - файлы')
#     descr = models.TextField(blank=True, null=True, db_comment='Описание')
#     renter_type = models.ForeignKey(RenterType, models.SET_DEFAULT, default=RenterType.default_pk, db_comment='Тип арендатора')
#     renter_phone = models.DecimalField(max_digits=11, decimal_places=0, blank=True, null=True, db_comment='Номер телефона')
#
#     class Meta:
#         managed = True
#         ordering = ['renter_name']
#         db_table = 'renter'
#         db_table_comment = 'Информация об арендаторах'
#         verbose_name = "Арендатор"
#         verbose_name_plural = "Арендаторы"
#
#     def __str__(self):
#         return f'{self.renter_name}'

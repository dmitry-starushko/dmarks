import base64
from decimal import Decimal
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.conf import settings
from django.db.models import Index, Q, F
from markets.enums import OutletState, FUS, NotificationType
from markets.validators import Validators


class DbItem(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract: bool = True


# -- DmUser ---------------------------------------------------------------------------------------

class DmUserManager(BaseUserManager):
    def create_user(self, phone, password, email, **extra_fields):
        Validators.phone(phone)
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

    @property
    def confirmed(self):
        return hasattr(self, 'aux_data') and self.aux_data.confirmed


class File(DbItem):
    file_name = models.CharField(max_length=512)  # -- имя файла --
    file_content = models.BinaryField()  # -- двоичный образ файла --

    class Meta:
        verbose_name = "Файл"
        verbose_name_plural = "Файлы"
        constraints = [models.CheckConstraint(check=~Q(file_name=''), name="File non-empty name")]

    def __str__(self):
        return f'Файл {self.file_name}'

    @property
    def as_dictionary(self):
        return {
            'file_name': self.file_name,
            'file_content_b64': base64.b64encode(self.file_content).decode('ascii')
        }


class AuxUserData(DbItem):
    user = models.OneToOneField(DmUser, on_delete=models.CASCADE, related_name='aux_data')  # -- ассоциированный пользователь --
    confirmed = models.BooleanField(default=False)  # -- данные подтверждены администрацией --
    itn = models.CharField(max_length=12, unique=True, validators=[Validators.itn])  # -- ИНН --
    usr_le_extract = models.OneToOneField(File, related_name='usr_le_extract', on_delete=models.SET_NULL, null=True)  # -- выписка из ЕСГРЮЛ, Unified State Register of Legal Entities --
    passport_image = models.OneToOneField(File, related_name='passport_image', on_delete=models.SET_NULL, null=True)  # -- скан паспорта --
    promo_image = models.ImageField(upload_to='renters/%Y/%m/%d', null=True)  # картинка
    promo_text = models.TextField(max_length=2048, default='')  # промо-текст

    class Meta:
        verbose_name = "Доп. данные"
        verbose_name_plural = "Доп. данные"
        constraints = [models.CheckConstraint(check=Q(itn__regex=Validators.ITN), name="ITN regex")]

    def __str__(self):
        return f'Данные "{self.user}"'

    def delete(self, *args, **kwargs):
        if self.usr_le_extract is not None:
            self.usr_le_extract.delete()
        if self.passport_image is not None:
            self.passport_image.delete()
        super().delete(*args, **kwargs)

    @property
    def image(self):
        return self.promo_image if self.promo_image else settings.DEF_MK_IMG


# -- Legacy data ----------------------------------------------------------------------------------

class LocalityType(models.Model):
    type_name = models.CharField(unique=True, db_comment='Наименование типа')
    descr = models.TextField(blank=True, null=True, db_comment='Описание')

    @classmethod
    def default_pk(cls):
        item, _ = cls.objects.get_or_create(type_name=FUS.NS)
        return item.pk

    class Meta:
        managed = True
        ordering = ['type_name']
        db_table = 'locality_type'
        db_table_comment = 'Типы населенных пунктов'
        verbose_name = "Тип локации"
        verbose_name_plural = "Типы локаций"
        constraints = [models.CheckConstraint(check=~Q(type_name=''), name="LocalityType non-empty name")]

    def __str__(self):
        return f'{self.type_name}'


class Locality(models.Model):
    locality_name = models.CharField(db_comment='Наименование населенного пункта')
    locality_type = models.ForeignKey(LocalityType, models.SET_DEFAULT, default=LocalityType.default_pk, db_comment='Тип населенного пункта')
    parent = models.ForeignKey('self', models.SET_NULL, blank=True, null=True, db_comment='Родительская запись. Иерархическое подчинение')
    descr = models.TextField(blank=True, null=True, db_comment='Описание')

    @classmethod
    def default_pk(cls):
        item, _ = cls.objects.get_or_create(locality_name=FUS.NS)
        return item.pk

    class Meta:
        managed = True
        ordering = ['locality_name']
        db_table = 'locality'
        db_table_comment = 'Населенные пункты'
        verbose_name = "Локация"
        verbose_name_plural = "Локации"
        constraints = [models.CheckConstraint(check=~Q(locality_name=''), name="Locality non-empty name")]

    def __str__(self):
        return f'{self.locality_name}'


class MarketFireProtection(models.Model):
    fp_name = models.CharField(unique=True, db_comment='Наименование противопожарной системы')
    descr = models.TextField(blank=True, null=True, db_comment='Описание')

    @classmethod
    def default_pk(cls):
        item, _ = cls.objects.get_or_create(fp_name=FUS.NS)
        return item.pk

    class Meta:
        managed = True
        ordering = ['fp_name']
        db_table = 'market_fire_protection'
        db_table_comment = 'Наличие и состав противопожарных систем'
        verbose_name = "Тип противопожарной системы"
        verbose_name_plural = "Типы противопожарных систем"
        constraints = [models.CheckConstraint(check=~Q(fp_name=''), name="MarketFireProtection non-empty name")]

    def __str__(self):
        return f'{self.fp_name}'


class MarketProfitability(models.Model):
    profitability_name = models.CharField(unique=True, db_comment='Наименование категории рентабельности рынка')
    descr = models.TextField(blank=True, null=True, db_comment='Описание')

    @classmethod
    def default_pk(cls):
        item, _ = cls.objects.get_or_create(profitability_name=FUS.NS)
        return item.pk

    class Meta:
        managed = True
        ordering = ['profitability_name']
        db_table = 'market_profitability'
        db_table_comment = 'Категория рентабельности рынка'
        verbose_name = "Категория рентабельности рынка"
        verbose_name_plural = "Категории рентабельности рынка"
        constraints = [models.CheckConstraint(check=~Q(profitability_name=''), name="MarketProfitability non-empty name")]

    def __str__(self):
        return f'{self.profitability_name}'


class MarketType(models.Model):
    type_name = models.CharField(unique=True, db_comment='Наименование типа рынка')
    descr = models.TextField(blank=True, null=True, db_comment='Описание')

    @classmethod
    def default_pk(cls):
        item, _ = cls.objects.get_or_create(type_name=FUS.NS)
        return item.pk

    class Meta:
        managed = True
        ordering = ['type_name']
        db_table = 'market_type'
        db_table_comment = 'Типы рынков'
        verbose_name = "Тип рынка"
        verbose_name_plural = "Типы рынка"
        constraints = [models.CheckConstraint(check=~Q(type_name=''), name="MarketType non-empty name")]

    def __str__(self):
        return f'{self.type_name}'


class StreetType(models.Model):
    type_name = models.CharField(unique=True, db_comment='Наименование типа улиц (сокращенное)')
    descr = models.TextField(blank=True, null=True, db_comment='Описание (полное наименование)')

    @classmethod
    def default_pk(cls):
        item, _ = cls.objects.get_or_create(type_name=FUS.NS)
        return item.pk

    class Meta:
        managed = True
        ordering = ['type_name']
        db_table = 'street_type'
        db_table_comment = 'Типы улиц'
        verbose_name = "Тип улицы"
        verbose_name_plural = "Типы улиц"
        constraints = [models.CheckConstraint(check=~Q(type_name=''), name="StreetType non-empty name")]

    def __str__(self):
        return f'{self.type_name}'


class TradePlaceType(models.Model):
    type_name_choices = {
        OutletState.UNKNOWN: FUS.NS,
        OutletState.AVAILABLE_FOR_BOOKING: 'Свободно',
        OutletState.UNAVAILABLE_FOR_BOOKING: 'Не сдаётся в аренду',
        OutletState.TEMPORARILY_UNAVAILABLE_FOR_BOOKING: 'Временно не сдается в аренду',
        OutletState.BOOKED: 'Забронировано',
        OutletState.RENTED: 'Занято'
    }
    type_name = models.CharField(unique=True, max_length=10, choices=type_name_choices.items(), db_comment='Наименование типа занятости торгового места')
    color = models.CharField(max_length=7, default='#ffffff', validators=[Validators.css_color], db_comment='Цвет в формате #ffffff')
    wall_color = models.CharField(max_length=8, default='0xffffff', validators=[Validators.hex], db_comment='Цвет стен ТМ в формате 0xffffff, для 3D')
    roof_color = models.CharField(max_length=8, default='0xffffff', validators=[Validators.hex], db_comment='Цвет крыш ТМ в формате 0xffffff, для 3D')
    descr = models.TextField(blank=True, null=True, db_comment='Опиcание')

    @classmethod
    def default_pk(cls):
        item, _ = cls.objects.get_or_create(type_name=OutletState.UNKNOWN)
        return item.pk

    class Meta:
        managed = True
        ordering = ['type_name']
        db_table = 'trade_place_type'
        db_table_comment = 'Типы занятости торгового места'
        verbose_name = "Тип занятости ТМ"
        verbose_name_plural = "Типы занятости ТМ"
        constraints = [
            models.CheckConstraint(check=Q(type_name__in=[i.value for i in OutletState]), name="TradePlaceType name from set"),
            models.CheckConstraint(check=Q(color__regex=Validators.CSS), name="TradePlaceType color regex"),
            models.CheckConstraint(check=Q(wall_color__regex=Validators.HEX), name="TradePlaceType wall_color regex"),
            models.CheckConstraint(check=Q(roof_color__regex=Validators.HEX), name="TradePlaceType roof_color regex"),
        ]

    def __str__(self):
        return f'{self.get_type_name_display()}'

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
        item, _ = cls.objects.get_or_create(sector_name=FUS.NS)
        return item.pk

    class Meta:
        managed = True
        ordering = ['sector_name']
        db_table = 'trade_sector'
        db_table_comment = 'Сектора рынков'
        verbose_name = "Сектор"
        verbose_name_plural = "Секторы"
        constraints = [
            models.CheckConstraint(check=~Q(sector_name=''), name="TradeSector non-empty name"),
            models.CheckConstraint(check=Q(color__regex=Validators.CSS), name="TradeSector color regex"),
            models.CheckConstraint(check=Q(wall_color__regex=Validators.HEX), name="TradeSector wall_color regex"),
            models.CheckConstraint(check=Q(roof_color__regex=Validators.HEX), name="TradeSector roof_color regex"),
        ]

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
        item, _ = cls.objects.get_or_create(type_name=FUS.NS)
        return item.pk

    class Meta:
        managed = True
        ordering = ['type_name']
        db_table = 'trade_spec_type'
        db_table_comment = 'Типы специализации торгового места'
        verbose_name = "Тип специализации ТМ"
        verbose_name_plural = "Типы специализации ТМ"
        constraints = [
            models.CheckConstraint(check=~Q(type_name=''), name="TradeSpecType non-empty name"),
            models.CheckConstraint(check=Q(color__regex=Validators.CSS), name="TradeSpecType color regex"),
            models.CheckConstraint(check=Q(wall_color__regex=Validators.HEX), name="TradeSpecType wall_color regex"),
            models.CheckConstraint(check=Q(roof_color__regex=Validators.HEX), name="TradeSpecType roof_color regex"),
        ]

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
    descr = models.TextField(blank=True, null=True, db_comment='Описание')

    @classmethod
    def default_pk(cls):
        item, _ = cls.objects.get_or_create(type_name=FUS.NS)
        return item.pk

    class Meta:
        managed = True
        ordering = ['type_name']
        db_table = 'trade_type'
        db_table_comment = 'Типы торгового места'
        verbose_name = "Тип ТМ"
        verbose_name_plural = "Типы ТМ"
        constraints = [models.CheckConstraint(check=~Q(type_name=''), name="TradeType non-empty name")]

    def __str__(self):
        return f'{self.type_name}'


class Market(models.Model):
    market_id = models.CharField(max_length=3, unique=True, validators=[Validators.market_id], db_comment='Уникальный идентификатор рынка')
    market_name = models.CharField(max_length=128, db_comment='Наименование рынка')
    additional_name = models.CharField(max_length=128, blank=True, default='', db_comment='Дополнительное наименование')
    market_type = models.ForeignKey(MarketType, models.SET_DEFAULT, default=MarketType.default_pk, db_comment='id - тип рынка')
    branch = models.CharField(max_length=12, default=FUS.NS, db_comment='Отделение')

    profitability = models.ForeignKey(MarketProfitability, models.SET_DEFAULT, default=MarketProfitability.default_pk, db_comment='id - категория рентабельности')
    infr_fire_protection = models.ForeignKey(MarketFireProtection, models.SET_DEFAULT, default=MarketFireProtection.default_pk, db_comment='id - противопожарные системы')
    infr_parking = models.SmallIntegerField(default=0, validators=[MinValueValidator(0)], db_comment='Кол-во парковок')
    infr_entrance = models.SmallIntegerField(default=0, validators=[MinValueValidator(0)], db_comment='Кол-во подъездов')
    infr_restroom = models.SmallIntegerField(default=0, validators=[MinValueValidator(0)], db_comment='Кол-во санузлов')
    infr_storage = models.SmallIntegerField(default=0, validators=[MinValueValidator(0)], db_comment='Кол-во складских помещений')
    infr_water_pipes = models.BooleanField(default=False, db_comment='Наличие водопровода')
    infr_sewerage = models.BooleanField(default=False, db_comment='Наличие канализации')
    infr_sewerage_type = models.CharField(max_length=64, default=FUS.NS, db_comment='Тип канализации')

    lat = models.FloatField(default=0.0, validators=[MinValueValidator(-90.0), MaxValueValidator(90.0)], db_comment='Широта - координата рынка')
    lng = models.FloatField(default=0.0, validators=[MinValueValidator(-180.0), MaxValueValidator(180.0)], db_comment='Долгота - координата рынка')
    geo_city = models.ForeignKey(Locality, models.SET_DEFAULT, default=Locality.default_pk, db_comment='Город - id')
    geo_district = models.ForeignKey(Locality, models.SET_DEFAULT, default=Locality.default_pk, related_name='markets_geo_district_set', db_comment='Район - id')
    geo_street_type = models.ForeignKey(StreetType, models.SET_DEFAULT, default=StreetType.default_pk, db_comment='Тип улицы - id')
    geo_street = models.CharField(max_length=64, default=FUS.NS, db_comment='Наименование улицы')
    geo_house = models.CharField(max_length=50, default=FUS.NS, db_comment='Дом')
    geo_index = models.CharField(max_length=10, validators=[Validators.postal_code], default=FUS.NS, db_comment='Индекс')
    market_area = models.FloatField(default=0.0, db_comment='Общая площадь рынка')

    schedule = models.TextField(default=FUS.NS, db_column='shedule', db_comment='График работы')
    ads = models.TextField(default=FUS.NS, db_comment='Реклама')
    images: models.QuerySet

    class Meta:
        managed = True
        ordering = ['market_name', 'additional_name']
        db_table = 'markets'
        db_table_comment = 'Информация о рынках'
        verbose_name = "Рынок"
        verbose_name_plural = "Рынки"
        constraints = [
            models.CheckConstraint(check=Q(market_id__regex=Validators.MID), name="market_id regex"),
            models.CheckConstraint(check=Q(geo_index__regex=Validators.POC), name="postal code regex"),
            models.CheckConstraint(check=~Q(market_name=''), name="non-empty market_name"),
            models.CheckConstraint(check=~Q(branch=''), name="non-empty branch"),
            models.CheckConstraint(check=~Q(geo_street=''), name="non-empty street"),
            models.CheckConstraint(check=~Q(geo_house=''), name="non-empty house"),
            models.CheckConstraint(check=~Q(schedule=''), name="non-empty schedule"),
            models.CheckConstraint(check=Q(infr_parking__gte=0), name="non-negative parking"),
            models.CheckConstraint(check=Q(infr_entrance__gte=0), name="non-negative entrance"),
            models.CheckConstraint(check=Q(infr_restroom__gte=0), name="non-negative restroom"),
            models.CheckConstraint(check=Q(infr_storage__gte=0), name="non-negative storage"),
            models.CheckConstraint(check=Q(market_area__gte=0.0), name="non-negative market area"),
            models.CheckConstraint(check=Q(lat__gte=-90.0) & Q(lat__lte=90.0), name="lat range"),
            models.CheckConstraint(check=Q(lng__gte=-180.0) & Q(lat__lte=180.0), name="lng range")
        ]

    def __str__(self):
        return self.mk_full_name

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
        return f'{self.geo_city.locality_type} {self.geo_city}, {self.geo_street_type} {self.geo_street}, {self.geo_house}'

    @property
    def mk_geo_index(self):
        return settings.DISP_RE.sub(' ', self.geo_index).strip()

    @property
    def mk_full_name(self):
        return f'Рынок {self.mk_market_name}{f' ({self.mk_additional_name})' if self.mk_additional_name else ''}'

    @property
    def mk_full_address(self):
        return f'{self.mk_geo_index} {self.mk_geo_full_address}'


class SvgSchema(models.Model):
    market = models.ForeignKey(Market, on_delete=models.CASCADE, related_name="schemes", db_comment='id рынка')
    floor = models.CharField(default=FUS.NS, db_comment='Этаж схемы объекта')
    order = models.IntegerField(default=0, db_comment='Поле для упорядочивания схем')
    svg_schema = models.TextField(default='', db_comment='svg объекта')

    class Meta:
        managed = True
        ordering = ['order']
        db_table = 'svg_schema'
        verbose_name = "Схема"
        verbose_name_plural = "Схемы"
        models.CheckConstraint(check=~Q(floor=''), name="non-empty floor"),

    def __str__(self):
        return f'Схема #{self.id}, уровень "{self.floor}", рынок "{self.market}"'


class MkImage(DbItem):  # -- Market images
    image = models.ImageField(upload_to='markets/%Y/%m/%d')  # картинка
    market = models.ForeignKey(Market, related_name="images", on_delete=models.CASCADE)  # рынок

    class Meta:
        verbose_name = "Изображение"
        verbose_name_plural = "Изображения"

    def __str__(self):
        return f'Фотография рынка #{self.market.id}'


class MarketPhone(DbItem):  # -- Market phones
    phone = models.CharField(unique=True, validators=[Validators.phone], max_length=20)
    market = models.ForeignKey(Market, related_name="phones", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Телефон"
        verbose_name_plural = "Телефоны"
        constraints = [models.CheckConstraint(check=Q(phone__regex=Validators.PNE), name="Market phone regex")]

    def __str__(self):
        return f'{self.phone}'


class MarketEmail(DbItem):  # -- Market emails
    email = models.EmailField(unique=True, max_length=255)
    market = models.ForeignKey(Market, related_name="emails", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "EMail"
        verbose_name_plural = "EMail"

    def __str__(self):
        return f'{self.email}'


class TradePlace(models.Model):
    market = models.ForeignKey(Market, on_delete=models.CASCADE, related_name="trade_places", db_comment='Уникальный идентификатор рынка\r\n')
    location_number = models.CharField(unique=True, validators=[Validators.outlet_number], db_comment='Номер торгового места')
    location_row = models.CharField(default=FUS.NS, db_comment='Ряд торгового места')
    price = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal(0.0), validators=[MinValueValidator(0.0)], db_comment='Стоимость аренды торгового места в месяц')
    street_vending = models.BooleanField(default=False, db_comment='Возможность выносной торговли')

    trade_type = models.ForeignKey(TradeType, on_delete=models.SET_DEFAULT, default=TradeType.default_pk, db_comment='Тип торгового места')
    trade_place_type = models.ForeignKey(TradePlaceType, on_delete=models.SET_DEFAULT, default=TradePlaceType.default_pk, db_comment='Занятость торгового места')
    trade_spec_type_id_act = models.ForeignKey(TradeSpecType, on_delete=models.SET_DEFAULT, default=TradeSpecType.default_pk, db_column='trade_spec_type_id_act', related_name='tradeplace_trade_spec_type_id_act_set', db_comment='Специализация торгового места (фактическая)')
    trade_spec_type_id_rec = models.ForeignKey(TradeSpecType, on_delete=models.SET_DEFAULT, default=TradeSpecType.default_pk, db_column='trade_spec_type_id_rec', db_comment='Специализация торгового места (рекомендованная)')
    location_sector = models.ForeignKey(TradeSector, on_delete=models.SET_DEFAULT, default=TradeSector.default_pk, db_comment='id сектор торгового места')
    scheme = models.ForeignKey(SvgSchema, related_name="outlets", on_delete=models.SET_NULL, null=True)
    rented_by = models.ForeignKey(DmUser, on_delete=models.RESTRICT, null=True, db_comment='кем арендовано')

    meas_area = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)], db_comment='Площадь места')
    meas_length = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)], db_comment='Длина места')
    meas_height = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)], db_comment='Высота места')
    meas_width = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)], db_comment='Ширина места')

    impr_electricity = models.BooleanField(default=False, db_comment='Наличие электричества')
    impr_heat_supply = models.BooleanField(default=False, db_comment='Наличие теплоснабжения')
    impr_air_conditioning = models.BooleanField(default=False, db_comment='Наличие кондиционирования')
    impr_plumbing = models.BooleanField(default=False, db_comment='Наличие водопровода')
    impr_sewerage = models.BooleanField(default=False, db_comment='Наличие канализации')
    impr_drains = models.BooleanField(default=False, db_comment='Наличие стоков')
    impr_internet = models.BooleanField(default=False, db_comment='Подключение к сети интернет')
    impr_internet_type_id = models.SmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(2)], db_comment='Тип подключения к сети интернет (0 - не заполнено, 1 - проводной, 2 - беспроводной)')
    impr_add_equipment = models.BooleanField(default=False, db_comment='Наличие стендов, мебели')
    impr_fridge = models.BooleanField(default=False, db_comment='Наличие холодильных установок')
    impr_shopwindow = models.BooleanField(default=False, db_comment='Наличие витрин')

    class Meta:
        managed = True
        ordering = ['location_number']
        db_table = 'trade_place'
        db_table_comment = 'Торговые места'
        indexes = [Index(fields=["location_number"], name='index_by_number')]
        verbose_name = "Торговое место"
        verbose_name_plural = "Торговые места"
        constraints = [
            models.CheckConstraint(check=Q(location_number__regex=Validators.ONM), name="location number regex"),
            models.CheckConstraint(check=Q(impr_internet_type_id__gte=0) & Q(impr_internet_type_id__lte=2), name="internet_type_id range"),
            models.CheckConstraint(check=Q(meas_area__gte=0.0), name="non-negative area"),
            models.CheckConstraint(check=Q(meas_length__gte=0.0), name="non-negative length"),
            models.CheckConstraint(check=Q(meas_height__gte=0.0), name="non-negative height"),
            models.CheckConstraint(check=Q(meas_width__gte=0.0), name="non-negative width"),
            models.CheckConstraint(check=Q(price__gte=0.0), name="non-negative price")]

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


# -- Events & Notifications -----------------------------------------------------------------------

class Notification(DbItem):
    type_choices = {
        NotificationType.INFORMATION: 'Информация',
        NotificationType.WARNING: 'Важная информация',
        NotificationType.ALERT: 'Критическая информация',
    }
    user = models.ForeignKey(DmUser, on_delete=models.CASCADE, related_name='notifications', null=True, blank=True)  # NULL for broadcast
    published = models.DateField()
    unpublished = models.DateField()
    calendar_event = models.BooleanField()
    type = models.CharField(max_length=4, choices=type_choices.items(), default=NotificationType.INFORMATION)
    text = models.TextField()
    attachment = models.OneToOneField(File, on_delete=models.PROTECT, null=True, blank=True)
    read = models.BooleanField(default=False)

    class Meta:
        managed = True
        ordering = ['published']
        indexes = [
            Index(fields=["published"], name='index_by_published'),
            Index(fields=["unpublished"], name='index_by_unpublished')]
        verbose_name = "Уведомление"
        verbose_name_plural = "Уведомления"
        constraints = [
            models.CheckConstraint(check=~Q(text=''), name="non-empty notification text"),
            models.CheckConstraint(check=~(Q(user__isnull=True) & Q(read=True)), name="broadcast notification can not be 'read'"),
            models.CheckConstraint(check=Q(type__in=[i.value for i in NotificationType]), name="type values from set"),
            models.CheckConstraint(check=Q(published__lt=F('unpublished')), name="unpublished after published")]

    def __str__(self):
        return f'{'Событие' if self.calendar_event else 'Уведомление'} #{self.id}'

    def delete(self, *args, **kwargs):
        attachment = self.attachment
        super().delete(*args, **kwargs)
        if attachment is not None:
            attachment.delete()

    @property
    def broadcast(self):
        return self.user is None


# -- Contacts -------------------------------------------------------------------------------------

class Contact(DbItem):
    title = models.CharField(max_length=128, default=FUS.NS)
    image = models.ImageField(upload_to='contacts/%Y/%m/%d')  # картинка
    address = models.CharField(max_length=256, default=FUS.NS)
    city = models.ForeignKey(Locality, models.SET_DEFAULT, default=Locality.default_pk)
    district = models.ForeignKey(Locality, models.SET_DEFAULT, default=Locality.default_pk, related_name='another_contact_set')

    class Meta:
        ordering = ['title']
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'

    def __str__(self):
        return f'{self.title}'

    @property
    def qr_text(self):
        return '\n'.join([self.title] + [str(r) for r in self.phones.all()] + [str(r) for r in self.emails.all()])


class ContactPhone(DbItem):  # -- Contact phones
    phone = models.CharField(unique=True, validators=[Validators.phone], max_length=20)
    contact = models.ForeignKey(Contact, related_name='phones', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Контактный телефон'
        verbose_name_plural = 'Контактные телефоны'
        constraints = [models.CheckConstraint(check=Q(phone__regex=Validators.PNE), name="Contact phone regex")]

    def __str__(self):
        return f'{self.phone}'


class ContactEmail(DbItem):  # -- Contact emails
    email = models.EmailField(unique=True, max_length=255)
    contact = models.ForeignKey(Contact, related_name='emails', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Контактный email'
        verbose_name_plural = 'Контактные email'

    def __str__(self):
        return f'{self.email}'


# -- NG Data --------------------------------------------------------------------------------------

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


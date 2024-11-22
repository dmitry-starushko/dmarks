from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.conf import settings
from django.db.models import Index
from markets.models_mixins import TpMixin, MkMixin


class Validators:
    @staticmethod
    def _rxv(rx: str, msg: str):
        return RegexValidator(regex=rx, message=msg)

    @staticmethod
    def css_color(value):
        return Validators._rxv("^#[0-9a-fA-F]{6}$", "Ожидается значение в формате #ffffff")(value)

    @staticmethod
    def hex(value):
        return Validators._rxv("^0x[0-9a-fA-F]{1,6}$", "Ожидается значение в формате 0xffffff")(value)

    @staticmethod
    def outlet_number(value):
        return Validators._rxv("^[0-9]{9}[а-яё]{0,1}$", "Ожидается значение в формате 999999999[a]")(value)


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


# -- Legacy data ----------------------------------------------------------------------------------


class Booking(models.Model):
    trade_place = models.ForeignKey('TradePlace', models.DO_NOTHING, related_name="bookings", db_comment='Идентификатор торгового места')
    descr = models.TextField(blank=True, null=True, db_comment='Описание')
    date_transaction = models.DateTimeField(db_comment='Дата создания записи')
    booking_status = models.TextField(db_comment='Статус бронирования')  # This field type is a guess.
    booking_status_case = models.TextField(blank=True, null=True, db_comment='Причина изменения статуса (например, причина отказа)')
    booking_files = models.JSONField(blank=True, null=True, db_comment='Файлы для бронирования')
    user = models.ForeignKey('User', models.CASCADE, null=True, blank=True, db_column='user', db_comment='Кто забронировал (в старой версии БД)')
    booked_by = models.ForeignKey(DmUser, models.CASCADE, null=True, blank=True, related_name="bookings", db_column='ng_user', db_comment='Кто забронировал (NULL для старых броней)')
    renter_id = models.DecimalField(max_digits=32, decimal_places=0, blank=True, null=True, db_comment='Арендатор (пользователь из внешнего источника, надо искать в базе)')
    location_number = models.CharField(blank=True, null=True, db_comment='Номер торгового места (по странной логике ДЦТ, сюда падают номера которых нет в базе -- мы даем отлуп)')

    class Meta:
        managed = True
        ordering = ['-date_transaction']
        db_table = 'booking'
        db_table_comment = 'Бронирование торговых мест'
        verbose_name = "Бронирование ТМ"
        verbose_name_plural = "Бронирования ТМ"

    def __str__(self):
        return f'Бронирование {self.id}'

    @property
    def scheme(self):
        return SvgSchema.objects.get(pk=self.trade_place.location_floor)


class ChangeLog(models.Model):
    date_change = models.DateTimeField()
    title_change = models.CharField(max_length=128)
    text_change = models.TextField()
    link_change = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'change_log'
        db_table_comment = 'Журнал внесенных изменений'

    def __str__(self):
        return f'Запись журнала изменений {self.id}'


class ContractStatusType(models.Model):
    id = models.SmallAutoField(primary_key=True)
    type_name = models.CharField(db_comment='Наименование типа специализации торгового места')
    descr = models.TextField(blank=True, null=True, db_comment='Описание')

    class Meta:
        managed = True
        ordering = ['type_name']
        db_table = 'contract_status_type'
        db_table_comment = 'Типы статусов договоров'
        verbose_name = "Тип статуса договора"
        verbose_name_plural = "Типы статуса договора"

    def __str__(self):
        return f'{self.type_name}'


class GlobalConfig(models.Model):
    param_name = models.CharField(db_comment='Имя параметра')
    param_data = models.TextField(blank=True, null=True, db_comment='Значение параметра')
    descr = models.TextField(blank=True, null=True, db_comment='Описание')

    class Meta:
        managed = True
        ordering = ['param_name']
        db_table = 'global_config'
        db_table_comment = 'Глобальная конфигурация системы'
        verbose_name = "Настройка"
        verbose_name_plural = "Настройки"

    def __str__(self):
        return f'{self.param_name}'


class Help(models.Model):
    header = models.CharField(max_length=1000, db_comment='Заголовок')
    html = models.TextField(db_comment='Содержание')
    order_num = models.FloatField(db_comment='Порядок сортировки')
    subj = models.CharField(max_length=100, db_comment='Тема')

    class Meta:
        managed = True
        db_table = 'help'
        db_table_comment = 'Помощь'

    def __str__(self):
        return f'{self.header}'


class ImportData(models.Model):
    descr = models.TextField(blank=True, null=True, db_comment='Описание')
    import_status = models.TextField(db_comment='Статус импорта')  # This field type is a guess.
    date_transaction = models.DateTimeField(db_comment='Дата транзакции')
    user_id_transaction = models.ForeignKey('User', models.CASCADE, null=True, db_column='user_id_transaction', db_comment='id создателя (в старой БД)')
    created_by = models.ForeignKey(DmUser, models.CASCADE, null=True, blank=True, db_comment='id создателя (NULL для старых записей)')
    filename = models.CharField(db_comment='Имя импортируемого файла')
    filepath_server = models.CharField(db_comment='Путь импортируемого файла на сервере')
    date_modify = models.DateTimeField(blank=True, null=True, db_comment='Дата измения транзакции')
    params = models.JSONField(blank=True, null=True, db_comment='Настройки импорта')
    result = models.JSONField(blank=True, null=True, db_comment='Результат импорта')

    class Meta:
        managed = True
        ordering = ['-date_transaction']
        db_table = 'import_data'
        db_table_comment = 'Данные о загрузке xml файлов (импорт из 1С)\r\nid - это номер транзакции импорта. Он один в started, stopped, imported\r\nStarted после удачной загрузки файла начинается испорт данных в таблицу\r\nImported - при удачной загрузке\r\nStopped - при возникновении ошибки (exception)\r\nЕсли статус остается Stared после завершения импорта - считать импор неудашимся, посольку удавшийся импорт идентифицирует статус Imported'

    def __str__(self):
        return f'{self.id}'


class ImportMarket(MkMixin, models.Model):
    id_transaction = models.IntegerField(db_comment='id транзакции')
    market_name = models.CharField(max_length=500, db_comment='Наименование рынка')
    internal_id = models.CharField(max_length=50, blank=True, null=True, db_comment='Внутренний код рынка')
    market_type_name = models.CharField(blank=True, null=True, db_comment='Тип рынка, если нет в базе')
    profitability_name = models.CharField(blank=True, null=True, db_comment='Категория рентабельности, если нет в базе')
    infr_parking = models.SmallIntegerField(blank=True, null=True, db_comment='Кол-во парковок')
    infr_entrance = models.SmallIntegerField(blank=True, null=True, db_comment='Кол-во подъездов')
    infr_restroom = models.SmallIntegerField(blank=True, null=True, db_comment='Кол-во санузлов')
    infr_water_pipes = models.BooleanField(blank=True, null=True, db_comment='Наличие водопровода')
    infr_sewerage = models.BooleanField(blank=True, null=True, db_comment='Наличие канализации')
    infr_sewerage_type = models.CharField(max_length=1000, blank=True, null=True, db_comment='Тип канализации')
    infr_storage = models.SmallIntegerField(blank=True, null=True, db_comment='Кол-во складских помещений')
    infr_fire_protection_name = models.CharField(blank=True, null=True, db_comment='Противопожарные системы, если нет в базе')
    info_statement_forms = models.TextField(blank=True, null=True, db_comment='Информация о формах зявлений')
    info_statement_files = models.JSONField(blank=True, null=True, db_comment='Формы заявлений - файлы')
    info_contracts = models.TextField(blank=True, null=True, db_comment='Информация о типовых договорах')
    info_contracts_files = models.JSONField(blank=True, null=True, db_comment='Формы типовых договоров - файлы')
    info_contracts_req = models.TextField(blank=True, null=True, db_comment='Информация о требованиях для оформления договоров/талонов')
    info_contracts_req_files = models.JSONField(blank=True, null=True, db_comment='Требованиях для оформления договоров/талонов - файлы')
    info_constitutive = models.TextField(blank=True, null=True, db_comment='Информация о копиях правоустанавливающих документов дочернего предприятия')
    info_constitutive_files = models.JSONField(blank=True, null=True, db_comment='Копии правоустанавливающих документов дочернего предприятия - файлы')
    info_other_docs = models.TextField(blank=True, null=True, db_comment='Информация о других документах')
    info_other_docs_files = models.JSONField(blank=True, null=True, db_comment='Другие документы - файлы')
    geo_city_name = models.CharField(blank=True, null=True, db_comment='Город, если нет в базе')
    geo_district_name = models.CharField(blank=True, null=True, db_comment='Район, если нет в базе')
    geo_street_type_name = models.CharField(blank=True, null=True, db_comment='Тип улицы, если нет в базе')
    geo_street = models.TextField(blank=True, null=True, db_comment='Наименование улицы')
    geo_house = models.CharField(max_length=50, blank=True, null=True, db_comment='Дом')
    phone = models.CharField(max_length=255, blank=True, null=True, db_comment='Телефоны')
    email = models.CharField(max_length=255, blank=True, null=True, db_comment='Электронные адреса')
    schedule = models.CharField(blank=True, null=True, db_column='shedule', db_comment='График работы')
    ads = models.TextField(blank=True, null=True, db_comment='Реклама')
    market_square = models.FloatField(blank=True, null=True, db_comment='Общая площадь рынка')
    market_count = models.IntegerField(blank=True, null=True, db_comment='Кол-во торговых мест')
    activity = models.TextField(blank=True, null=True, db_comment='Возможные виды деятельности')
    additional = models.JSONField(blank=True, null=True, db_comment='Дополнительные поля')
    date_transaction = models.DateTimeField(blank=True, null=True, db_comment='Дата создания записи')
    id_user_transaction = models.IntegerField(blank=True, null=True, db_comment='id создателя')
    market_id = models.CharField(max_length=50, blank=True, null=True, db_comment='Уникальный идентификатор рынка')
    market_id_char = models.CharField(max_length=50, blank=True, null=True, db_comment='Идентификатор записи markets.id')
    citizen_appeal = models.TextField(blank=True, null=True, db_comment='Информация для обращения граждан/ФЛП')
    market_type = models.ForeignKey('MarketType', models.DO_NOTHING, blank=True, null=True, db_comment='Тип рынка, если есть в базе')
    profitability = models.ForeignKey('MarketProfitability', models.DO_NOTHING, blank=True, null=True, db_comment='Категория рентабельности, если есть в базе')
    geo_city = models.ForeignKey('Locality', models.DO_NOTHING, blank=True, null=True, db_comment='Город, если есть в базе')
    geo_district = models.ForeignKey('Locality', models.DO_NOTHING, related_name='importmarkets_geo_district_set', blank=True, null=True, db_comment='Район, если есть в базе')
    geo_street_type = models.ForeignKey('StreetType', models.DO_NOTHING, blank=True, null=True, db_comment='Тип улицы, если есть в базе')
    infr_fire_protection = models.ForeignKey('MarketFireProtection', models.DO_NOTHING, blank=True, null=True, db_comment='Противопожарные системы,, если есть в базе')
    geo_index = models.CharField(max_length=10, blank=True, null=True, db_comment='Индекс')
    lat = models.FloatField(blank=True, null=True, db_comment='Широта')
    lng = models.FloatField(blank=True, null=True, db_comment='Долгота')
    additional_name = models.CharField(max_length=1000, blank=True, null=True, db_comment='Дополнительное наименование')
    descr = models.TextField(blank=True, null=True, db_comment='Описание импортируемой записи')
    to_import = models.BooleanField(blank=True, null=True, db_comment='Импортировать запись? true - да, false - нет')
    geo_full_address = models.CharField(blank=True, null=True, db_comment='Полный адрес через запятую')
    market_id_internal = models.IntegerField(blank=True, null=True, db_comment='id рынка, который импортировался успешно в таблицу markets')

    class Meta:
        managed = True
        db_table = 'import_markets'
        db_table_comment = 'Временная таблица для импорта рынка'

    def __str__(self):
        return f'{self.id}'


class ImportTradePlace(TpMixin, models.Model):
    id_transaction = models.IntegerField()
    market = models.ForeignKey('Market', models.DO_NOTHING, blank=True, null=True, db_comment='Уникальный идентификатор рынка')
    trade_type = models.ForeignKey('TradeType', models.DO_NOTHING, db_comment='Тип торгового места')
    meas_area = models.FloatField(blank=True, null=True, db_comment='Площадь места')
    meas_length = models.FloatField(blank=True, null=True, db_comment='Длина места')
    meas_width = models.FloatField(blank=True, null=True, db_comment='Ширина места')
    meas_height = models.FloatField(blank=True, null=True, db_comment='Высота места')
    impr_electricity = models.BooleanField(blank=True, null=True, db_comment='Наличие электричества')
    impr_heat_supply = models.BooleanField(blank=True, null=True, db_comment='Наличие теплоснабжения')
    impr_air_conditioning = models.BooleanField(blank=True, null=True, db_comment='Наличие кондиционирования')
    impr_plumbing = models.BooleanField(blank=True, null=True, db_comment='Наличие водопровода')
    impr_sewerage = models.BooleanField(blank=True, null=True, db_comment='Наличие канализации')
    impr_drains = models.BooleanField(blank=True, null=True, db_comment='Наличие стоков')
    impr_internet = models.BooleanField(blank=True, null=True, db_comment='Подключение к сети интернет')
    impr_internet_type_id = models.SmallIntegerField(blank=True, null=True, db_comment='Тип подключения к сети интернет (1 - проводной, 2 - беспроводной)')
    impr_add_equipment = models.BooleanField(blank=True, null=True, db_comment='Наличие стендов, мебели')
    impr_fridge = models.BooleanField(blank=True, null=True, db_comment='Наличие холодильных установок')
    impr_shopwindow = models.BooleanField(blank=True, null=True, db_comment='Наличие витрин')
    trade_place_type = models.ForeignKey('TradePlaceType', models.DO_NOTHING, blank=True, null=True, db_comment='Наименование типа занятости торгового места')
    price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, db_comment='Стоимость аренды торгового места в месяц')
    trade_spec_type_rec = models.CharField(blank=True, null=True, db_comment='Специализация торгового места (рекомендованная)')
    trade_spec_type_act = models.CharField(blank=True, null=True, db_comment='Специализация торгового места (фактическая)')
    street_vending = models.BooleanField(blank=True, null=True, db_comment='Возможность выносной торговли')
    contract_date_start = models.DateField(blank=True, null=True, db_comment='Дата начала договора')
    contract_date_end = models.DateField(blank=True, null=True, db_comment='Дата окончания договора')
    contract_status_type = models.ForeignKey(ContractStatusType, models.DO_NOTHING, blank=True, null=True, db_comment='Статус договора')
    contract_copy_info = models.CharField(blank=True, null=True, db_comment='Информация о копии договора')
    contract_copy_files = models.JSONField(blank=True, null=True, db_comment='Файлы договора')
    receiv_state = models.BooleanField(blank=True, null=True, db_comment='Наличие дебиторской задолженности на текущий месяц')
    receiv_amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, db_comment='Размер дебиторской задолженности')
    pay_electricity = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, db_comment='Оплата электричества')
    pay_heat_supply = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, db_column='pay_heat_supplay', db_comment='Оплата услуг теплоснабжения')
    pay_air_conditioning = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, db_comment='Оплата за кондиционер')
    pay_plumbing = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, db_comment='Оплата услуг водоснабжения')
    pay_sewerage = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, db_comment='Оплата услуг водоотведения')
    pay_drains = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, db_comment='Оплата наличия стоков')
    pay_internet = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, db_comment='Оплата интернета')
    pay_add_equipment = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, db_comment='Аренда стендов, мебели')
    pay_fridge = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, db_comment='Аренда холодильных установок')
    pay_shopwindows = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, db_comment='Аренда витрин')
    location_sector = models.ForeignKey('TradeSector', models.DO_NOTHING, blank=True, null=True, db_comment='id сектор торгового места')
    location_row = models.CharField(blank=True, null=True, db_comment='Ряд торгового места')
    location_floor = models.SmallIntegerField(blank=True, null=True, db_comment='Этаж торгового места')
    location_number = models.CharField(unique=True, blank=True, null=True, validators=[Validators.outlet_number], db_comment='Номер торгового места')
    renter_name = models.CharField(blank=True, null=True, db_comment='Наименование арендатора')
    legal_doc_info = models.CharField(blank=True, null=True, db_comment='Информация об уставных документах')
    legal_doc_files = models.JSONField(blank=True, null=True, db_comment='Уставные документы - файлы')
    additional = models.JSONField(blank=True, null=True, db_comment='Дополнительные поля')
    date_transaction = models.DateTimeField(blank=True, null=True, db_comment='Дата транзакции')
    id_user_transaction = models.IntegerField(blank=True, null=True, db_comment='id создателя')
    renter_type = models.ForeignKey('RenterType', models.DO_NOTHING, blank=True, null=True, db_comment='Тип арендатора')
    to_import = models.BooleanField(blank=True, null=True, db_comment='Импортировать запись? true - да, false - нет')
    speciality_recommend = models.JSONField(blank=True, null=True, db_comment='Специализация торгового места (рекомендованная)')
    speciality_actual = models.JSONField(blank=True, null=True, db_comment='Специализация торгового места (фактическая)')
    trade_place = models.ForeignKey('TradePlace', models.DO_NOTHING, blank=True, null=True, db_comment='id импортируемого ТМ из таблицы trade_place')
    active_contract = models.BooleanField(blank=True, null=True, db_comment='Наличие договора аренды')
    activities_type = models.JSONField(blank=True, null=True, db_comment='Возможные виды деятельности')
    tp_id_internal = models.IntegerField(blank=True, null=True, db_comment='id рынка, который импортировался успешно в таблицу trade_place')
    descr = models.TextField(blank=True, null=True, db_comment='Описание импортируемой записи')
    contract_rent = models.ForeignKey('TradeContract', models.DO_NOTHING, blank=True, null=True, db_comment='Информация о договорах аренды')
    renter = models.ForeignKey('Renter', models.DO_NOTHING, blank=True, null=True, db_comment='id - текущий арендатор')

    class Meta:
        managed = True
        db_table = 'import_trade_place'
        db_table_comment = 'Импорт - торговые места'

    def __str__(self):
        return f'{self.id}'


class Locality(models.Model):
    locality_name = models.CharField(db_comment='Наименование населенного пункта')
    locality_type = models.ForeignKey('LocalityType', models.DO_NOTHING, blank=True, null=True, db_comment='Тип населенного пункта')
    descr = models.TextField(blank=True, null=True, db_comment='Описание')
    parent = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True, db_comment='Родительская запись. Иерархическое подчинение')

    @classmethod
    def default_pk(cls):
        loc, flag = cls.objects.get_or_create(locality_name="Не указано")
        return loc.pk

    class Meta:
        managed = True
        ordering = ['locality_name']
        db_table = 'locality'
        db_table_comment = 'Населенные пункты'
        verbose_name = "Локация"
        verbose_name_plural = "Локации"

    def __str__(self):
        return f'{self.locality_name}'


class LocalityType(models.Model):
    id = models.SmallAutoField(primary_key=True)
    type_name = models.CharField(db_comment='Наименование типа')
    descr = models.TextField(blank=True, null=True, db_comment='Описание')

    class Meta:
        managed = True
        ordering = ['type_name']
        db_table = 'locality_type'
        db_table_comment = 'Типы населенных пунктов'
        verbose_name = "Тип локации"
        verbose_name_plural = "Типы локаций"

    def __str__(self):
        return f'{self.type_name}'


class MarketFireProtection(models.Model):
    fp_name = models.CharField(db_comment='Наименование противопожарной системы')
    descr = models.TextField(blank=True, null=True, db_comment='Описание')

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
    id = models.SmallIntegerField(primary_key=True)
    profitability_name = models.CharField(db_comment='Наименование категории рентабельности рынка')
    descr = models.TextField(blank=True, null=True, db_comment='Описание')

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
    id = models.SmallAutoField(primary_key=True)
    type_name = models.CharField(db_comment='Наименование типа рынка')
    descr = models.TextField(blank=True, null=True, db_comment='Описание')

    class Meta:
        managed = True
        ordering = ['type_name']
        db_table = 'market_type'
        db_table_comment = 'Типы рынков'
        verbose_name = "Тип рынка"
        verbose_name_plural = "Типы рынка"

    def __str__(self):
        return f'{self.type_name}'


class Market(MkMixin, models.Model):
    market_name = models.CharField(max_length=1000, db_comment='Наименование рынка')
    internal_id = models.CharField(max_length=50, blank=True, null=True, db_comment='Внутренний код рынка')
    market_type = models.ForeignKey(MarketType, models.DO_NOTHING, db_comment='id - тип рынка')
    profitability = models.ForeignKey(MarketProfitability, models.DO_NOTHING, blank=True, null=True, db_comment='id - категория рентабельности')
    infr_parking = models.SmallIntegerField(blank=True, null=True, db_comment='Кол-во парковок')
    infr_entrance = models.SmallIntegerField(blank=True, null=True, db_comment='Кол-во подъездов')
    infr_restroom = models.SmallIntegerField(blank=True, null=True, db_comment='Кол-во санузлов')
    infr_water_pipes = models.BooleanField(blank=True, null=True, db_comment='Наличие водопровода')
    infr_sewerage = models.BooleanField(blank=True, null=True, db_comment='Наличие канализации')
    infr_sewerage_type = models.CharField(max_length=1000, blank=True, null=True, db_comment='Тип канализации')
    infr_storage = models.SmallIntegerField(blank=True, null=True, db_comment='Кол-во складских помещений')
    infr_fire_protection = models.ForeignKey(MarketFireProtection, models.DO_NOTHING, blank=True, null=True, db_comment='id - противопожарные системы')
    info_statement_forms = models.TextField(blank=True, null=True, db_comment='Информация о формах заявлений')
    info_statement_files = models.JSONField(blank=True, null=True, db_comment='Формы заявлений - файлы')
    info_contracts = models.TextField(blank=True, null=True, db_comment='Информация о типовых договорах')
    info_contracts_files = models.JSONField(blank=True, null=True, db_comment='Формы типовых договоров - файлы')
    info_contracts_req = models.TextField(blank=True, null=True, db_comment='Информация о требованиях для оформления договоров/талонов')
    info_contracts_req_files = models.JSONField(blank=True, null=True, db_comment='Требованиях для оформления договоров/талонов - файлы')
    info_constitutive = models.TextField(blank=True, null=True, db_comment='Информация о копиях правоустанавливающих документов дочернего предприятия')
    info_constitutive_files = models.JSONField(blank=True, null=True, db_comment='Копии правоустанавливающих документов дочернего предприятия - файлы')
    info_other_docs = models.TextField(blank=True, null=True, db_comment='Информация о других документах')
    info_other_docs_files = models.JSONField(blank=True, null=True, db_comment='Другие документы - файлы')
    geo_city = models.ForeignKey(Locality, models.DO_NOTHING, blank=False, null=False, db_comment='Город - id', default=Locality.default_pk)
    geo_district = models.ForeignKey(Locality, models.DO_NOTHING, related_name='markets_geo_district_set', blank=False, null=False, db_comment='Район - id', default=Locality.default_pk)
    geo_street_type = models.ForeignKey('StreetType', models.DO_NOTHING, blank=True, null=True, db_comment='Тип улицы - id')
    geo_street = models.TextField(blank=True, null=True, db_comment='Наименование улицы')
    geo_house = models.CharField(max_length=50, blank=True, null=True, db_comment='Дом')
    phone = models.CharField(max_length=255, blank=True, null=True, db_comment='Телефоны')
    email = models.CharField(max_length=255, blank=True, null=True, db_comment='Электронные адреса')
    schedule = models.TextField(blank=True, null=True, db_column='shedule', db_comment='График работы')
    ads = models.TextField(blank=True, null=True, db_comment='Реклама')
    market_square = models.FloatField(blank=True, null=True, db_comment='Общая площадь рынка')
    market_count = models.IntegerField(blank=True, null=True, db_comment='Кол-во торговых мест')
    activity = models.TextField(blank=True, null=True, db_comment='Возможные виды деятельности')
    additional = models.JSONField(blank=True, null=True, db_comment="Дополнительные поля в формате {'param_name' : 'param_value'}")
    schema_file = models.JSONField(blank=True, null=True, db_comment='Файл c данными отображения')
    market_id = models.CharField(max_length=3, blank=True, null=True, db_comment='Уникальный идентификатор рынка')
    market_id_char = models.CharField(max_length=50, blank=True, null=True, db_comment='Уникальный идентификатор рынка согласно шаблону 001010001')
    citizen_appeal = models.TextField(blank=True, null=True, db_comment='Информация для обращения граждан/ФЛП')
    lat = models.FloatField(blank=True, null=True, db_comment='Широта - координата рынка')
    lng = models.FloatField(blank=True, null=True, db_comment='Долгота - координата рынка')
    additional_name = models.CharField(max_length=1000, blank=True, null=True, db_comment='Дополнительное наименование')
    geo_index = models.CharField(max_length=10, blank=True, null=True, db_comment='Индекс')
    geo_full_address = models.CharField(blank=True, null=True, db_comment='Полный адрес через запятую')
    images: models.QuerySet

    @property
    def image(self):
        first_img = self.images.first()
        return first_img.image if first_img else settings.DEF_MK_IMG

    class Meta:
        managed = True
        ordering = ['market_name', 'additional_name']
        db_table = 'markets'
        db_table_comment = 'Информация о рынках'
        verbose_name = "Рынок"
        verbose_name_plural = "Рынки"

    def __str__(self):
        return f'{self.market_name}:{self.additional_name}'


class Migration(models.Model):
    version = models.CharField(primary_key=True, max_length=180)
    apply_time = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'migration'

    def __str__(self):
        return f'{self.id}'


class Renter(models.Model):
    renter_name = models.CharField(db_comment='Наименование арендатора')
    legal_doc_info = models.CharField(blank=True, null=True, db_comment='Информация об уставных документах')
    legal_doc_files = models.JSONField(blank=True, null=True, db_comment='Уставные документы - файлы')
    descr = models.TextField(blank=True, null=True, db_comment='Описание')
    renter_type = models.ForeignKey('RenterType', models.DO_NOTHING, db_comment='Тип арендатора')
    renter_phone = models.DecimalField(max_digits=11, decimal_places=0, blank=True, null=True, db_comment='Номер телефона')

    class Meta:
        managed = True
        ordering = ['renter_name']
        db_table = 'renter'
        db_table_comment = 'Информация об арендаторах'
        verbose_name = "Арендатор"
        verbose_name_plural = "Арендаторы"

    def __str__(self):
        return f'{self.renter_name}'


class RenterType(models.Model):
    id = models.SmallAutoField(primary_key=True)
    type_name = models.CharField(db_comment='Наименование типа арендатора')
    descr = models.TextField(blank=True, null=True, db_comment='Описание')

    class Meta:
        managed = True
        ordering = ['type_name']
        db_table = 'renter_type'
        db_table_comment = 'Тип арендатора'
        verbose_name = "Тип арендатора"
        verbose_name_plural = "Типы арендаторов"

    def __str__(self):
        return f'{self.type_name}'


class StreetType(models.Model):
    id = models.SmallAutoField(primary_key=True)
    type_name = models.CharField(db_comment='Наименование типа улиц (сокращенное)')
    descr = models.TextField(blank=True, null=True, db_comment='Описание (полное наименование)')

    class Meta:
        managed = True
        ordering = ['type_name']
        db_table = 'street_type'
        db_table_comment = 'Типы улиц'
        verbose_name = "Тип улицы"
        verbose_name_plural = "Типы улиц"

    def __str__(self):
        return f'{self.type_name}'


class SvgSchema(models.Model):
    order = models.IntegerField(blank=False, null=False, default=0, db_comment='Поле для упорядочивания схем')
    svg_schema = models.TextField(blank=True, null=True, db_comment='svg объекта')
    market = models.ForeignKey(Market, models.DO_NOTHING, related_name="schemes", blank=True, null=True, db_comment='id рынка')  # TODO models.CASCADE
    descr = models.TextField(blank=True, null=True, db_comment='Описание')
    source_file = models.CharField(blank=True, null=True, db_comment='Имя загруженного файла')
    floor = models.CharField(blank=True, null=True, db_comment='Этаж схемы объекта')

    class Meta:
        managed = True
        ordering = ['order']
        db_table = 'svg_schema'
        verbose_name = "Схема"
        verbose_name_plural = "Схемы"

    def __str__(self):
        return f'Схема #{self.id}, уровень "{self.floor}", рынок "{self.market}"'


class TradeContract(models.Model):
    date_start = models.DateField(blank=True, null=True, db_comment='Дата начала договора')
    date_end = models.DateField(blank=True, null=True, db_comment='Дата окончания договора')
    contract_status_type = models.ForeignKey(ContractStatusType, models.DO_NOTHING, db_comment='id статус договора')
    copy_info = models.CharField(blank=True, null=True, db_comment='Информация о копии договора')
    copy_files = models.JSONField(blank=True, null=True, db_comment='Файлы договора')
    active_contract = models.BooleanField(blank=True, null=True, db_comment='Наличие договора аренды')
    contract_num = models.CharField(blank=True, null=True, db_comment='Номер договора')

    class Meta:
        managed = True
        db_table = 'trade_contract'
        db_table_comment = 'Информация о договорах аренды'
        verbose_name = "Договор аренды"
        verbose_name_plural = "Договоры аренды"

    def __str__(self):
        return f'Контракт {self.id}'


class TradePlace(TpMixin, models.Model):
    market = models.ForeignKey(Market, models.DO_NOTHING, related_name="trade_places", db_comment='Уникальный идентификатор рынка\r\n')
    trade_type = models.ForeignKey('TradeType', models.DO_NOTHING, db_comment='Тип торгового места')
    meas_area = models.FloatField(blank=True, null=True, db_comment='Площадь места')
    meas_length = models.FloatField(blank=True, null=True, db_comment='Длина места')
    meas_height = models.FloatField(blank=True, null=True, db_comment='Высота места')
    impr_electricity = models.BooleanField(blank=True, null=True, db_comment='Наличие электричества')
    impr_heat_supply = models.BooleanField(blank=True, null=True, db_comment='Наличие теплоснабжения')
    impr_air_conditioning = models.BooleanField(blank=True, null=True, db_comment='Наличие кондиционирования')
    impr_plumbing = models.BooleanField(blank=True, null=True, db_comment='Наличие водопровода')
    impr_sewerage = models.BooleanField(blank=True, null=True, db_comment='Наличие канализации')
    impr_drains = models.BooleanField(blank=True, null=True, db_comment='Наличие стоков')
    impr_internet = models.BooleanField(blank=True, null=True, db_comment='Подключение к сети интернет')
    impr_internet_type_id = models.SmallIntegerField(blank=True, null=True, db_comment='Тип подключения к сети интернет (0 - не заполнено, 1 - проводной, 2 - беспроводной)')
    impr_add_equipment = models.BooleanField(blank=True, null=True, db_comment='Наличие стендов, мебели')
    impr_fridge = models.BooleanField(blank=True, null=True, db_comment='Наличие холодильных установок')
    impr_shopwindow = models.BooleanField(blank=True, null=True, db_comment='Наличие витрин')
    trade_place_type = models.ForeignKey('TradePlaceType', models.DO_NOTHING, db_comment='Занятость торгового места')
    price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, db_comment='Стоимость аренды торгового места в месяц')
    trade_spec_type_id_rec = models.ForeignKey('TradeSpecType', models.DO_NOTHING, db_column='trade_spec_type_id_rec', blank=True, null=True, db_comment='Специализация торгового места (рекомендованная)')
    trade_spec_type_id_act = models.ForeignKey('TradeSpecType', models.DO_NOTHING, db_column='trade_spec_type_id_act', related_name='tradeplace_trade_spec_type_id_act_set', blank=True, null=True, db_comment='Специализация торгового места (фактическая)')
    street_vending = models.BooleanField(blank=True, null=True, db_comment='Возможность выносной торговли')
    contract_rent = models.ForeignKey(TradeContract, models.DO_NOTHING, blank=True, null=True, db_comment='Информация о договорах аренды')
    receiv_state = models.BooleanField(blank=True, null=True, db_comment='Наличие дебиторской задолженности на текущий месяц')
    receiv_amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, db_comment='Размер дебиторской задолженности')
    pay_electricity = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, db_comment='Оплата электричества')
    pay_heat_supply = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, db_column='pay_heat_supplay', db_comment='Оплата услуг теплоснабжения')
    pay_air_conditioning = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, db_comment='Оплата за кондиционер')
    pay_plumbing = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, db_comment='Оплата услуг водоснабжения')
    pay_sewerage = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, db_comment='Оплата услуг водоотведения')
    pay_drains = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, db_comment='Оплата наличия стоков')
    pay_internet = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, db_comment='Оплата интернета')
    pay_add_equipment = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, db_comment='Аренда стендов, мебели')
    pay_fridge = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, db_comment='Аренда холодильных установок')
    pay_shopwindows = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, db_comment='Аренда витрин')
    location_sector = models.ForeignKey('TradeSector', models.DO_NOTHING, db_comment='id сектор торгового места')
    location_row = models.CharField(blank=True, null=True, db_comment='Ряд торгового места')
    location_floor = models.SmallIntegerField(blank=True, null=True, db_comment='Этаж торгового места')
    location_number = models.CharField(unique=True, blank=True, null=True, validators=[Validators.outlet_number], db_comment='Номер торгового места')
    renter = models.ForeignKey(Renter, models.DO_NOTHING, blank=True, null=True, db_comment='id - текущий арендатор')
    additional = models.JSONField(blank=True, null=True, db_comment='Дополнительные поля')
    meas_width = models.FloatField(blank=True, null=True, db_comment='Ширина места')
    internal_id = models.CharField(blank=True, null=True, db_comment='Текстовый код')
    speciality_recommend = models.JSONField(blank=True, null=True, db_comment='Специализация торгового места (рекомендованная)')
    speciality_actual = models.JSONField(blank=True, null=True, db_comment='Специализация торгового места (фактическая)')
    activities_type = models.JSONField(blank=True, null=True, db_comment='Возможные виды деятельности')

    class Meta:
        managed = True
        ordering = ['location_number']
        db_table = 'trade_place'
        db_table_comment = 'Торговые места'
        indexes = [
            Index(fields=["location_number"], include=["location_floor"], name='index_by_number'),
            Index(fields=["location_floor"], include=["location_number"], name='index_by_storey'),
        ]
        verbose_name = "Торговое место"
        verbose_name_plural = "Торговые места"

    def __str__(self):
        return f'ТМ #{self.id} <{self.location_number}>'


class TradePlaceType(models.Model):
    id = models.SmallAutoField(primary_key=True)
    type_name = models.CharField(db_comment='Наименование типа занятости торгового места')
    descr = models.TextField(blank=True, null=True, db_comment='Опиcание')
    color = models.CharField(max_length=7, blank=True, null=True, validators=[Validators.css_color], db_comment='Цвет в формате #ffffff')
    wall_color = models.CharField(max_length=8, default='0xffffff', validators=[Validators.hex], db_comment='Цвет стен ТМ в формате 0xffffff, для 3D')
    roof_color = models.CharField(max_length=8, default='0xffffff', validators=[Validators.hex], db_comment='Цвет крыш ТМ в формате 0xffffff, для 3D')

    class Meta:
        managed = True
        ordering = ['type_name']
        db_table = 'trade_place_type'
        db_table_comment = 'Типы занятости торгового места'
        verbose_name = "Тип занятости ТМ"
        verbose_name_plural = "Типы занятости ТМ"

    @property
    def wall_color_css(self):
        return f'#{hex(int(self.wall_color, 16))[2:]}'

    @property
    def roof_color_css(self):
        return f'#{hex(int(self.roof_color, 16))[2:]}'

    def __str__(self):
        return f'{self.type_name}'


class TradeSector(models.Model):
    id = models.SmallAutoField(primary_key=True)
    sector_name = models.CharField(db_comment='Наименование сектора рынка')
    descr = models.TextField(blank=True, null=True, db_comment='Описание')

    class Meta:
        managed = True
        ordering = ['sector_name']
        db_table = 'trade_sector'
        db_table_comment = 'Сектора рынков'
        verbose_name = "Сектор"
        verbose_name_plural = "Секторы"

    def __str__(self):
        return f'{self.sector_name}'


class TradeSpecType(models.Model):
    id = models.SmallAutoField(primary_key=True)
    type_name = models.CharField(db_comment='Наименование типа специализации торгового места')
    descr = models.TextField(blank=True, null=True, db_comment='Описание')
    color = models.CharField(max_length=7, blank=True, null=True, db_comment='Цвет в формате #ffffff')
    wall_color = models.CharField(max_length=8, default='0xffffff', validators=[Validators.hex], db_comment='Цвет стен ТМ в формате 0xffffff, для 3D')
    roof_color = models.CharField(max_length=8, default='0xffffff', validators=[Validators.hex], db_comment='Цвет крыш ТМ в формате 0xffffff, для 3D')

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
    id = models.SmallAutoField(primary_key=True)
    type_name = models.CharField(db_comment='Наименование типа торгового места')
    type_num = models.SmallIntegerField(blank=True, null=True, db_comment='Код типа объекта')
    descr = models.TextField(blank=True, null=True, db_comment='Описание')

    class Meta:
        managed = True
        ordering = ['type_name']
        db_table = 'trade_type'
        db_table_comment = 'Типы торгового места'
        verbose_name = "Тип ТМ"
        verbose_name_plural = "Типы ТМ"

    def __str__(self):
        return f'{self.type_name}'


class User(models.Model):
    username = models.CharField(unique=True, max_length=255)
    auth_key = models.CharField(max_length=32)
    password_hash = models.CharField(max_length=255)
    password_reset_token = models.CharField(unique=True, max_length=255, blank=True, null=True)
    email = models.CharField(unique=True, max_length=255, blank=True, null=True)
    status = models.SmallIntegerField()
    created_at = models.IntegerField()
    updated_at = models.IntegerField()
    verification_token = models.CharField(max_length=255, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    ahash = models.CharField(max_length=32, blank=True, null=True, db_comment='Хеш для доступа по апи')
    fio = models.CharField(max_length=255, blank=True, null=True, db_comment='Фамилия Имя Отчество пользователя')
    areal = models.IntegerField(blank=True, null=True, db_comment='Ареал обитания. 0 - везде, 1 - только публичка')
    accept = models.DateTimeField(blank=True, null=True, db_comment='момент согласия с политикой конфиденциальности')

    class Meta:
        managed = True
        ordering = ['username']
        db_table = 'user'
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f'{self.username}'


class UserLogin(models.Model):
    uid = models.IntegerField()
    dat = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'user_login'

    def __str__(self):
        return f'{self.id}'


# -- NG Data --------------------------------------------------------------------------------------


class MkImage(DbItem):  # -- Market images
    image = models.ImageField(upload_to='markets/%Y/%m/%d')  # картинка
    market = models.ForeignKey(Market, related_name="images", on_delete=models.CASCADE)  # рынок

    class Meta:
        verbose_name = "Изображение"
        verbose_name_plural = "Изображения"

    def __str__(self):
        return f'Фотография рынка #{self.market.id}'


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


class RdcError(DbItem):  # -- Errors detected by Restore Database Consistency procedure
    object = models.CharField(max_length=250)  # -- источник --
    text = models.TextField()  # -- проблема --

    def __str__(self):
        return f'Ошибка "{self.id}"'

    class Meta:
        verbose_name = "Ошибка"
        verbose_name_plural = "Ошибки"


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

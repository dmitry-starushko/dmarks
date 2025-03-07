# Generated by Django 4.2.16 on 2024-12-22 06:59

from decimal import Decimal
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import markets.enums
import markets.models
import markets.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='DmUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('phone', models.CharField(max_length=16, unique=True)),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(default=markets.enums.FUS['NS'], max_length=128)),
                ('image', models.ImageField(upload_to='contacts/%Y/%m/%d')),
                ('address', models.CharField(default=markets.enums.FUS['NS'], max_length=256)),
            ],
            options={
                'verbose_name': 'Контакт',
                'verbose_name_plural': 'Контакты',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('file_name', models.CharField(max_length=512)),
                ('file_content', models.BinaryField()),
            ],
            options={
                'verbose_name': 'Файл',
                'verbose_name_plural': 'Файлы',
            },
        ),
        migrations.CreateModel(
            name='GlobalObservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('key', models.CharField(max_length=50, unique=True)),
                ('decimal', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=12)),
            ],
            options={
                'verbose_name': 'Значение',
                'verbose_name_plural': 'Значения',
            },
        ),
        migrations.CreateModel(
            name='Locality',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('locality_name', models.CharField(db_comment='Наименование населенного пункта')),
                ('descr', models.TextField(blank=True, db_comment='Описание', null=True)),
            ],
            options={
                'verbose_name': 'Локация',
                'verbose_name_plural': 'Локации',
                'db_table': 'locality',
                'db_table_comment': 'Населенные пункты',
                'ordering': ['locality_name'],
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='LocalityType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_name', models.CharField(db_comment='Наименование типа', unique=True)),
                ('descr', models.TextField(blank=True, db_comment='Описание', null=True)),
            ],
            options={
                'verbose_name': 'Тип локации',
                'verbose_name_plural': 'Типы локаций',
                'db_table': 'locality_type',
                'db_table_comment': 'Типы населенных пунктов',
                'ordering': ['type_name'],
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Market',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('market_id', models.CharField(db_comment='Уникальный идентификатор рынка', max_length=3, unique=True, validators=[markets.validators.Validators.market_id])),
                ('market_name', models.CharField(db_comment='Наименование рынка', max_length=128)),
                ('additional_name', models.CharField(blank=True, db_comment='Дополнительное наименование', default='', max_length=128)),
                ('branch', models.CharField(db_comment='Отделение', default=markets.enums.FUS['NS'], max_length=12)),
                ('infr_parking', models.SmallIntegerField(db_comment='Кол-во парковок', default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('infr_entrance', models.SmallIntegerField(db_comment='Кол-во подъездов', default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('infr_restroom', models.SmallIntegerField(db_comment='Кол-во санузлов', default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('infr_storage', models.SmallIntegerField(db_comment='Кол-во складских помещений', default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('infr_water_pipes', models.BooleanField(db_comment='Наличие водопровода', default=False)),
                ('infr_sewerage', models.BooleanField(db_comment='Наличие канализации', default=False)),
                ('infr_sewerage_type', models.CharField(db_comment='Тип канализации', default=markets.enums.FUS['NS'], max_length=64)),
                ('lat', models.FloatField(db_comment='Широта - координата рынка', default=0.0, validators=[django.core.validators.MinValueValidator(-90.0), django.core.validators.MaxValueValidator(90.0)])),
                ('lng', models.FloatField(db_comment='Долгота - координата рынка', default=0.0, validators=[django.core.validators.MinValueValidator(-180.0), django.core.validators.MaxValueValidator(180.0)])),
                ('geo_street', models.CharField(db_comment='Наименование улицы', default=markets.enums.FUS['NS'], max_length=64)),
                ('geo_house', models.CharField(db_comment='Дом', default=markets.enums.FUS['NS'], max_length=50)),
                ('geo_index', models.CharField(db_comment='Индекс', default=markets.enums.FUS['NS'], max_length=10, validators=[markets.validators.Validators.postal_code])),
                ('market_area', models.FloatField(db_comment='Общая площадь рынка', default=0.0)),
                ('schedule', models.TextField(db_column='shedule', db_comment='График работы', default=markets.enums.FUS['NS'])),
                ('ads', models.TextField(db_comment='Реклама', default=markets.enums.FUS['NS'])),
                ('geo_city', models.ForeignKey(db_comment='Город - id', default=markets.models.Locality.default_pk, on_delete=django.db.models.deletion.SET_DEFAULT, to='markets.locality')),
                ('geo_district', models.ForeignKey(db_comment='Район - id', default=markets.models.Locality.default_pk, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='markets_geo_district_set', to='markets.locality')),
            ],
            options={
                'verbose_name': 'Рынок',
                'verbose_name_plural': 'Рынки',
                'db_table': 'markets',
                'db_table_comment': 'Информация о рынках',
                'ordering': ['market_name', 'additional_name'],
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='MarketFireProtection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fp_name', models.CharField(db_comment='Наименование противопожарной системы', unique=True)),
                ('descr', models.TextField(blank=True, db_comment='Описание', null=True)),
            ],
            options={
                'verbose_name': 'Тип противопожарной системы',
                'verbose_name_plural': 'Типы противопожарных систем',
                'db_table': 'market_fire_protection',
                'db_table_comment': 'Наличие и состав противопожарных систем',
                'ordering': ['fp_name'],
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='MarketProfitability',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profitability_name', models.CharField(db_comment='Наименование категории рентабельности рынка', unique=True)),
                ('descr', models.TextField(blank=True, db_comment='Описание', null=True)),
            ],
            options={
                'verbose_name': 'Категория рентабельности рынка',
                'verbose_name_plural': 'Категории рентабельности рынка',
                'db_table': 'market_profitability',
                'db_table_comment': 'Категория рентабельности рынка',
                'ordering': ['profitability_name'],
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='MarketType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_name', models.CharField(db_comment='Наименование типа рынка', unique=True)),
                ('descr', models.TextField(blank=True, db_comment='Описание', null=True)),
            ],
            options={
                'verbose_name': 'Тип рынка',
                'verbose_name_plural': 'Типы рынка',
                'db_table': 'market_type',
                'db_table_comment': 'Типы рынков',
                'ordering': ['type_name'],
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Parameter',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('key', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('value', models.CharField(max_length=250)),
                ('preload', models.BooleanField(default=False)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Параметр',
                'verbose_name_plural': 'Параметры',
            },
        ),
        migrations.CreateModel(
            name='RdcError',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('object', models.CharField(max_length=250)),
                ('text', models.TextField()),
            ],
            options={
                'verbose_name': 'Ошибка',
                'verbose_name_plural': 'Ошибки',
            },
        ),
        migrations.CreateModel(
            name='StreetType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_name', models.CharField(db_comment='Наименование типа улиц (сокращенное)', unique=True)),
                ('descr', models.TextField(blank=True, db_comment='Описание (полное наименование)', null=True)),
            ],
            options={
                'verbose_name': 'Тип улицы',
                'verbose_name_plural': 'Типы улиц',
                'db_table': 'street_type',
                'db_table_comment': 'Типы улиц',
                'ordering': ['type_name'],
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='StuffAction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=64)),
                ('link', models.URLField(default='', max_length=512)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Операция',
                'verbose_name_plural': 'Операции',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='SvgSchema',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('floor', models.CharField(db_comment='Этаж схемы объекта', default=markets.enums.FUS['NS'])),
                ('order', models.IntegerField(db_comment='Поле для упорядочивания схем', default=0)),
                ('svg_schema', models.TextField(db_comment='svg объекта', default='')),
                ('market', models.ForeignKey(db_comment='id рынка', on_delete=django.db.models.deletion.CASCADE, related_name='schemes', to='markets.market')),
            ],
            options={
                'verbose_name': 'Схема',
                'verbose_name_plural': 'Схемы',
                'db_table': 'svg_schema',
                'ordering': ['order'],
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='TradePlaceType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_name', models.CharField(choices=[(markets.enums.OutletState['UNKNOWN'], markets.enums.FUS['NS']), (markets.enums.OutletState['AVAILABLE_FOR_BOOKING'], 'Свободно'), (markets.enums.OutletState['UNAVAILABLE_FOR_BOOKING'], 'Не сдаётся в аренду'), (markets.enums.OutletState['TEMPORARILY_UNAVAILABLE_FOR_BOOKING'], 'Временно не сдается в аренду'), (markets.enums.OutletState['BOOKED'], 'Забронировано'), (markets.enums.OutletState['RENTED'], 'Занято')], db_comment='Наименование типа занятости торгового места', max_length=10, unique=True)),
                ('color', models.CharField(db_comment='Цвет в формате #ffffff', default='#ffffff', max_length=7, validators=[markets.validators.Validators.css_color])),
                ('wall_color', models.CharField(db_comment='Цвет стен ТМ в формате 0xffffff, для 3D', default='0xffffff', max_length=8, validators=[markets.validators.Validators.hex])),
                ('roof_color', models.CharField(db_comment='Цвет крыш ТМ в формате 0xffffff, для 3D', default='0xffffff', max_length=8, validators=[markets.validators.Validators.hex])),
                ('descr', models.TextField(blank=True, db_comment='Опиcание', null=True)),
            ],
            options={
                'verbose_name': 'Тип занятости ТМ',
                'verbose_name_plural': 'Типы занятости ТМ',
                'db_table': 'trade_place_type',
                'db_table_comment': 'Типы занятости торгового места',
                'ordering': ['type_name'],
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='TradeSector',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sector_name', models.CharField(db_comment='Наименование сектора рынка', unique=True)),
                ('color', models.CharField(db_comment='Цвет в формате #ffffff', default='#ffffff', max_length=7, validators=[markets.validators.Validators.css_color])),
                ('wall_color', models.CharField(db_comment='Цвет стен ТМ в формате 0xffffff, для 3D', default='0xffffff', max_length=8, validators=[markets.validators.Validators.hex])),
                ('roof_color', models.CharField(db_comment='Цвет крыш ТМ в формате 0xffffff, для 3D', default='0xffffff', max_length=8, validators=[markets.validators.Validators.hex])),
                ('descr', models.TextField(blank=True, db_comment='Описание', null=True)),
            ],
            options={
                'verbose_name': 'Сектор',
                'verbose_name_plural': 'Секторы',
                'db_table': 'trade_sector',
                'db_table_comment': 'Сектора рынков',
                'ordering': ['sector_name'],
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='TradeSpecType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_name', models.CharField(db_comment='Наименование типа специализации торгового места', unique=True)),
                ('color', models.CharField(db_comment='Цвет в формате #ffffff', default='#ffffff', max_length=7, validators=[markets.validators.Validators.css_color])),
                ('wall_color', models.CharField(db_comment='Цвет стен ТМ в формате 0xffffff, для 3D', default='0xffffff', max_length=8, validators=[markets.validators.Validators.hex])),
                ('roof_color', models.CharField(db_comment='Цвет крыш ТМ в формате 0xffffff, для 3D', default='0xffffff', max_length=8, validators=[markets.validators.Validators.hex])),
                ('descr', models.TextField(blank=True, db_comment='Описание', null=True)),
            ],
            options={
                'verbose_name': 'Тип специализации ТМ',
                'verbose_name_plural': 'Типы специализации ТМ',
                'db_table': 'trade_spec_type',
                'db_table_comment': 'Типы специализации торгового места',
                'ordering': ['type_name'],
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='TradeType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_name', models.CharField(db_comment='Наименование типа торгового места', unique=True)),
                ('descr', models.TextField(blank=True, db_comment='Описание', null=True)),
            ],
            options={
                'verbose_name': 'Тип ТМ',
                'verbose_name_plural': 'Типы ТМ',
                'db_table': 'trade_type',
                'db_table_comment': 'Типы торгового места',
                'ordering': ['type_name'],
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='MkImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(upload_to='markets/%Y/%m/%d')),
                ('market', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='markets.market')),
            ],
            options={
                'verbose_name': 'Изображение',
                'verbose_name_plural': 'Изображения',
            },
        ),
        migrations.CreateModel(
            name='MarketPhone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('phone', models.CharField(max_length=20, unique=True)),
                ('market', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='phones', to='markets.market')),
            ],
            options={
                'verbose_name': 'Телефон',
                'verbose_name_plural': 'Телефоны',
            },
        ),
        migrations.CreateModel(
            name='MarketObservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('key', models.CharField(max_length=50)),
                ('decimal', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=12)),
                ('market', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='observations', to='markets.market')),
            ],
            options={
                'verbose_name': 'Значение',
                'verbose_name_plural': 'Значения',
            },
        ),
        migrations.CreateModel(
            name='MarketEmail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('market', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='emails', to='markets.market')),
            ],
            options={
                'verbose_name': 'EMail',
                'verbose_name_plural': 'EMail',
            },
        ),
        migrations.AddField(
            model_name='market',
            name='geo_street_type',
            field=models.ForeignKey(db_comment='Тип улицы - id', default=markets.models.StreetType.default_pk, on_delete=django.db.models.deletion.SET_DEFAULT, to='markets.streettype'),
        ),
        migrations.AddField(
            model_name='market',
            name='infr_fire_protection',
            field=models.ForeignKey(db_comment='id - противопожарные системы', default=markets.models.MarketFireProtection.default_pk, on_delete=django.db.models.deletion.SET_DEFAULT, to='markets.marketfireprotection'),
        ),
        migrations.AddField(
            model_name='market',
            name='market_type',
            field=models.ForeignKey(db_comment='id - тип рынка', default=markets.models.MarketType.default_pk, on_delete=django.db.models.deletion.SET_DEFAULT, to='markets.markettype'),
        ),
        migrations.AddField(
            model_name='market',
            name='profitability',
            field=models.ForeignKey(db_comment='id - категория рентабельности', default=markets.models.MarketProfitability.default_pk, on_delete=django.db.models.deletion.SET_DEFAULT, to='markets.marketprofitability'),
        ),
        migrations.AddField(
            model_name='locality',
            name='locality_type',
            field=models.ForeignKey(db_comment='Тип населенного пункта', default=markets.models.LocalityType.default_pk, on_delete=django.db.models.deletion.SET_DEFAULT, to='markets.localitytype'),
        ),
        migrations.AddField(
            model_name='locality',
            name='parent',
            field=models.ForeignKey(blank=True, db_comment='Родительская запись. Иерархическое подчинение', null=True, on_delete=django.db.models.deletion.SET_NULL, to='markets.locality'),
        ),
        migrations.CreateModel(
            name='ContactPhone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('phone', models.CharField(max_length=20, unique=True)),
                ('contact', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='phones', to='markets.contact')),
            ],
            options={
                'verbose_name': 'Контактный телефон',
                'verbose_name_plural': 'Контактные телефоны',
            },
        ),
        migrations.CreateModel(
            name='ContactEmail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('contact', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='emails', to='markets.contact')),
            ],
            options={
                'verbose_name': 'Контактный email',
                'verbose_name_plural': 'Контактные email',
            },
        ),
        migrations.AddField(
            model_name='contact',
            name='city',
            field=models.ForeignKey(default=markets.models.Locality.default_pk, on_delete=django.db.models.deletion.SET_DEFAULT, to='markets.locality'),
        ),
        migrations.AddField(
            model_name='contact',
            name='district',
            field=models.ForeignKey(default=markets.models.Locality.default_pk, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='another_contact_set', to='markets.locality'),
        ),
        migrations.CreateModel(
            name='AuxUserData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('confirmed', models.BooleanField(default=False)),
                ('itn', models.CharField(max_length=12, validators=[markets.validators.Validators.itn])),
                ('promo_image', models.ImageField(null=True, upload_to='renters/%Y/%m/%d')),
                ('promo_text', models.TextField(default='', max_length=2048)),
                ('passport_image', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='passport_image', to='markets.file')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='aux_data', to=settings.AUTH_USER_MODEL)),
                ('usr_le_extract', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='usr_le_extract', to='markets.file')),
            ],
            options={
                'verbose_name': 'Доп. данные',
                'verbose_name_plural': 'Доп. данные',
            },
        ),
        migrations.CreateModel(
            name='TradePlace',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location_number', models.CharField(db_comment='Номер торгового места', unique=True, validators=[markets.validators.Validators.outlet_number])),
                ('location_row', models.CharField(db_comment='Ряд торгового места', default=markets.enums.FUS['NS'])),
                ('price', models.DecimalField(db_comment='Стоимость аренды торгового места в месяц', decimal_places=2, default=Decimal('0'), max_digits=12, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('street_vending', models.BooleanField(db_comment='Возможность выносной торговли', default=False)),
                ('meas_area', models.FloatField(db_comment='Площадь места', default=0.0, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('meas_length', models.FloatField(db_comment='Длина места', default=0.0, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('meas_height', models.FloatField(db_comment='Высота места', default=0.0, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('meas_width', models.FloatField(db_comment='Ширина места', default=0.0, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('impr_electricity', models.BooleanField(db_comment='Наличие электричества', default=False)),
                ('impr_heat_supply', models.BooleanField(db_comment='Наличие теплоснабжения', default=False)),
                ('impr_air_conditioning', models.BooleanField(db_comment='Наличие кондиционирования', default=False)),
                ('impr_plumbing', models.BooleanField(db_comment='Наличие водопровода', default=False)),
                ('impr_sewerage', models.BooleanField(db_comment='Наличие канализации', default=False)),
                ('impr_drains', models.BooleanField(db_comment='Наличие стоков', default=False)),
                ('impr_internet', models.BooleanField(db_comment='Подключение к сети интернет', default=False)),
                ('impr_internet_type_id', models.SmallIntegerField(db_comment='Тип подключения к сети интернет (0 - не заполнено, 1 - проводной, 2 - беспроводной)', default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(2)])),
                ('impr_add_equipment', models.BooleanField(db_comment='Наличие стендов, мебели', default=False)),
                ('impr_fridge', models.BooleanField(db_comment='Наличие холодильных установок', default=False)),
                ('impr_shopwindow', models.BooleanField(db_comment='Наличие витрин', default=False)),
                ('location_sector', models.ForeignKey(db_comment='id сектор торгового места', default=markets.models.TradeSector.default_pk, on_delete=django.db.models.deletion.SET_DEFAULT, to='markets.tradesector')),
                ('market', models.ForeignKey(db_comment='Уникальный идентификатор рынка\r\n', on_delete=django.db.models.deletion.CASCADE, related_name='trade_places', to='markets.market')),
                ('rented_by', models.ForeignKey(db_comment='кем арендовано', null=True, on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
                ('scheme', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='outlets', to='markets.svgschema')),
                ('trade_place_type', models.ForeignKey(db_comment='Занятость торгового места', default=markets.models.TradePlaceType.default_pk, on_delete=django.db.models.deletion.SET_DEFAULT, to='markets.tradeplacetype')),
                ('trade_spec_type_id_act', models.ForeignKey(db_column='trade_spec_type_id_act', db_comment='Специализация торгового места (фактическая)', default=markets.models.TradeSpecType.default_pk, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='tradeplace_trade_spec_type_id_act_set', to='markets.tradespectype')),
                ('trade_spec_type_id_rec', models.ForeignKey(db_column='trade_spec_type_id_rec', db_comment='Специализация торгового места (рекомендованная)', default=markets.models.TradeSpecType.default_pk, on_delete=django.db.models.deletion.SET_DEFAULT, to='markets.tradespectype')),
                ('trade_type', models.ForeignKey(db_comment='Тип торгового места', default=markets.models.TradeType.default_pk, on_delete=django.db.models.deletion.SET_DEFAULT, to='markets.tradetype')),
            ],
            options={
                'verbose_name': 'Торговое место',
                'verbose_name_plural': 'Торговые места',
                'db_table': 'trade_place',
                'db_table_comment': 'Торговые места',
                'ordering': ['location_number'],
                'managed': True,
                'indexes': [models.Index(fields=['location_number'], name='index_by_number')],
            },
        ),
        migrations.AddConstraint(
            model_name='tradeplace',
            constraint=models.CheckConstraint(check=models.Q(('impr_internet_type_id__gte', 0), ('impr_internet_type_id__lte', 2)), name='internet_type_id range'),
        ),
        migrations.AddConstraint(
            model_name='tradeplace',
            constraint=models.CheckConstraint(check=models.Q(('meas_area__gte', 0.0)), name='non-negative area'),
        ),
        migrations.AddConstraint(
            model_name='tradeplace',
            constraint=models.CheckConstraint(check=models.Q(('meas_length__gte', 0.0)), name='non-negative length'),
        ),
        migrations.AddConstraint(
            model_name='tradeplace',
            constraint=models.CheckConstraint(check=models.Q(('meas_height__gte', 0.0)), name='non-negative height'),
        ),
        migrations.AddConstraint(
            model_name='tradeplace',
            constraint=models.CheckConstraint(check=models.Q(('meas_width__gte', 0.0)), name='non-negative width'),
        ),
        migrations.AddConstraint(
            model_name='tradeplace',
            constraint=models.CheckConstraint(check=models.Q(('price__gte', 0.0)), name='non-negative price'),
        ),
        migrations.AddConstraint(
            model_name='marketobservation',
            constraint=models.UniqueConstraint(fields=('key', 'market_id'), name='unique_key_per_market'),
        ),
        migrations.AddConstraint(
            model_name='market',
            constraint=models.CheckConstraint(check=models.Q(('infr_parking__gte', 0)), name='non-negative parking'),
        ),
        migrations.AddConstraint(
            model_name='market',
            constraint=models.CheckConstraint(check=models.Q(('infr_entrance__gte', 0)), name='non-negative entrance'),
        ),
        migrations.AddConstraint(
            model_name='market',
            constraint=models.CheckConstraint(check=models.Q(('infr_restroom__gte', 0)), name='non-negative restroom'),
        ),
        migrations.AddConstraint(
            model_name='market',
            constraint=models.CheckConstraint(check=models.Q(('infr_storage__gte', 0)), name='non-negative storage'),
        ),
        migrations.AddConstraint(
            model_name='market',
            constraint=models.CheckConstraint(check=models.Q(('market_area__gte', 0.0)), name='non-negative market area'),
        ),
        migrations.AddConstraint(
            model_name='market',
            constraint=models.CheckConstraint(check=models.Q(('lat__gte', -90.0), ('lat__lte', 90.0)), name='lat range'),
        ),
        migrations.AddConstraint(
            model_name='market',
            constraint=models.CheckConstraint(check=models.Q(('lng__gte', -180.0), ('lat__lte', 180.0)), name='lng range'),
        ),
    ]

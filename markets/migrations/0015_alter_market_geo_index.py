# Generated by Django 4.2.18 on 2025-02-26 12:34

from django.db import migrations, models
import markets.validators


class Migration(migrations.Migration):

    dependencies = [
        ('markets', '0014_delete_rdcerror'),
    ]

    operations = [
        migrations.AlterField(
            model_name='market',
            name='geo_index',
            field=models.CharField(db_comment='Индекс', default='000000', max_length=10, validators=[markets.validators.Validators.postal_code]),
        ),
    ]

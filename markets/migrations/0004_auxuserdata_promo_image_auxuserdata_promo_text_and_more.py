# Generated by Django 4.2.16 on 2024-12-07 14:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('markets', '0003_remove_tradeplace_pay_add_equipment_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='auxuserdata',
            name='promo_image',
            field=models.ImageField(null=True, upload_to='renters/%Y/%m/%d'),
        ),
        migrations.AddField(
            model_name='auxuserdata',
            name='promo_text',
            field=models.TextField(default='', max_length=2048),
        ),
        migrations.AddField(
            model_name='tradeplace',
            name='rented_by',
            field=models.ForeignKey(db_comment='кем арендовано', null=True, on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL),
        ),
    ]
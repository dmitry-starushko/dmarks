# Generated by Django 4.2.16 on 2024-10-02 12:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('markets', '0001_initial'),
    ]

    operations = [
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
    ]
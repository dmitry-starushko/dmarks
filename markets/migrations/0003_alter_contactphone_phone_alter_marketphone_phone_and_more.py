# Generated by Django 4.2.16 on 2024-12-22 12:04

from django.db import migrations, models
import markets.validators


class Migration(migrations.Migration):

    dependencies = [
        ('markets', '0002_auxuserdata_itn_regex_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactphone',
            name='phone',
            field=models.CharField(max_length=20, unique=True, validators=[markets.validators.Validators.phone]),
        ),
        migrations.AlterField(
            model_name='marketphone',
            name='phone',
            field=models.CharField(max_length=20, unique=True, validators=[markets.validators.Validators.phone]),
        ),
        migrations.AddConstraint(
            model_name='contactphone',
            constraint=models.CheckConstraint(check=models.Q(('phone__regex', '^\\+\\d{1,3}\\(\\d{3}\\)\\d{3}-\\d{2}-\\d{2}$')), name='Contact phone regex'),
        ),
        migrations.AddConstraint(
            model_name='marketphone',
            constraint=models.CheckConstraint(check=models.Q(('phone__regex', '^\\+\\d{1,3}\\(\\d{3}\\)\\d{3}-\\d{2}-\\d{2}$')), name='Market phone regex'),
        ),
    ]
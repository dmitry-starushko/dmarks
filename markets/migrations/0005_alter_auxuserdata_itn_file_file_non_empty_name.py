# Generated by Django 4.2.16 on 2024-12-25 19:37

from django.db import migrations, models
import markets.validators


class Migration(migrations.Migration):

    dependencies = [
        ('markets', '0004_notification_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auxuserdata',
            name='itn',
            field=models.CharField(max_length=12, unique=True, validators=[markets.validators.Validators.itn]),
        ),
        migrations.AddConstraint(
            model_name='file',
            constraint=models.CheckConstraint(check=models.Q(('file_name', ''), _negated=True), name='File non-empty name'),
        ),
    ]

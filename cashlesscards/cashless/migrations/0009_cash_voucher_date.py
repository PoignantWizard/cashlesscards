# Generated by Django 2.0.7 on 2018-08-26 13:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cashless', '0008_auto_20180826_1438'),
    ]

    operations = [
        migrations.AddField(
            model_name='cash',
            name='voucher_date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]

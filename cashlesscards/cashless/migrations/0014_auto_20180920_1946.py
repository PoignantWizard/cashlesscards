# Generated by Django 2.0.7 on 2018-09-20 18:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cashless', '0013_auto_20180920_1942'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customer',
            options={'ordering': ['surname', 'first_name'], 'permissions': (('can_add_customers', 'Create and edit customer accounts'),), 'verbose_name_plural': 'customers'},
        ),
        migrations.AlterField(
            model_name='voucherlink',
            name='last_applied',
            field=models.DateField(default=datetime.datetime(2017, 9, 20, 19, 46, 49, 52332)),
        ),
    ]

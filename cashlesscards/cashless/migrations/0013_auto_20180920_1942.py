# Generated by Django 2.0.7 on 2018-09-20 18:42

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cashless', '0012_auto_20180915_1637'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customer',
            options={'ordering': ['surname', 'first_name'], 'verbose_name_plural': 'customers'},
        ),
        migrations.AlterModelOptions(
            name='voucher',
            options={'ordering': ['voucher_name'], 'permissions': (('can_add_vouchers', 'Create and edit vouchers'),)},
        ),
        migrations.AlterField(
            model_name='transaction',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cashless.Customer'),
        ),
        migrations.AlterField(
            model_name='voucherlink',
            name='last_applied',
            field=models.DateField(default=datetime.datetime(2017, 9, 20, 19, 42, 22, 714098)),
        ),
    ]

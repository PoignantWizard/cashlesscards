# Generated by Django 2.0.7 on 2018-08-25 12:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cashless', '0005_auto_20180804_1931'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='transaction',
            options={'ordering': ['-transaction_time'], 'permissions': (('view_finance', 'Can view transaction log'),), 'verbose_name_plural': 'transactions'},
        ),
    ]

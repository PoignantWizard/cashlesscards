# Generated by Django 2.0.7 on 2018-08-25 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cashless', '0006_auto_20180825_1330'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='transaction_type',
            field=models.CharField(choices=[('credit', 'Credit'), ('debit', 'Debit')], default='credit', max_length=6),
        ),
    ]

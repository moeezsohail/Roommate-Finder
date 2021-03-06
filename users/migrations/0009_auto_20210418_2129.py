# Generated by Django 3.2 on 2021-04-19 01:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20210412_2042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='birthday',
            field=models.DateField(blank=True, default=datetime.date(2021, 4, 18)),
        ),
        migrations.AlterField(
            model_name='profile',
            name='budget_high',
            field=models.BigIntegerField(default=1000),
        ),
        migrations.AlterField(
            model_name='profile',
            name='noise_maximum',
            field=models.BigIntegerField(default=10),
        ),
        migrations.AlterField(
            model_name='profile',
            name='noise_minimum',
            field=models.BigIntegerField(default=1),
        ),
    ]

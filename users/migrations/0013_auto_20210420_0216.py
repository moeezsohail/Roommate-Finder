# Generated by Django 3.1.5 on 2021-04-20 02:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_merge_20210419_1839'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='birthday',
            field=models.DateField(blank=True, default=datetime.date(2021, 4, 20)),
        ),
    ]
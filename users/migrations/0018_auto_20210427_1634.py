# Generated by Django 3.1.5 on 2021-04-27 16:34

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0017_auto_20210427_1616'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='budget',
            field=models.BigIntegerField(default=500, max_length=3, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(1)]),
        ),
    ]
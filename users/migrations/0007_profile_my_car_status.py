# Generated by Django 3.1.5 on 2021-04-10 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20210410_2111'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='my_car_status',
            field=models.CharField(default=None, max_length=255, null=True),
        ),
    ]

# Generated by Django 3.1.5 on 2021-03-28 16:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('roommate_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='name',
            new_name='first_name',
        ),
    ]
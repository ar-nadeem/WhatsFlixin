# Generated by Django 3.0.7 on 2020-06-29 12:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0009_auto_20200629_1509'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='imdbPopularMovie',
            new_name='imdbPopMovie',
        ),
    ]

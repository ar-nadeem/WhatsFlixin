# Generated by Django 3.0.7 on 2020-07-26 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0016_auto_20200726_1016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imdbpopmovie',
            name='imdb_rating',
            field=models.FloatField(default='0.0', max_length=10),
        ),
    ]

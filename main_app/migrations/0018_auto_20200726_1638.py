# Generated by Django 3.0.7 on 2020-07-26 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0017_auto_20200726_1226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imdbpoptv',
            name='imdb_rating',
            field=models.FloatField(default='0.0', max_length=10),
        ),
        migrations.AlterField(
            model_name='imdbtopmovie',
            name='imdb_rating',
            field=models.FloatField(default='0.0', max_length=10),
        ),
        migrations.AlterField(
            model_name='imdbtoptv',
            name='imdb_rating',
            field=models.FloatField(default='0.0', max_length=10),
        ),
    ]

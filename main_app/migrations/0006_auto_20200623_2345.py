# Generated by Django 3.0.7 on 2020-06-23 18:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0005_auto_20200623_2337'),
    ]

    operations = [
        migrations.RenameField(
            model_name='imdbpopularmovie',
            old_name='rating',
            new_name='imdb_rating',
        ),
        migrations.RenameField(
            model_name='imdbtopmovie',
            old_name='rating',
            new_name='imdb_rating',
        ),
    ]

# Generated by Django 3.0.7 on 2020-07-26 05:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0015_auto_20200725_1204'),
    ]

    operations = [
        migrations.AddField(
            model_name='imdbpopmovie',
            name='imdb_url',
            field=models.CharField(default='#', max_length=500),
        ),
        migrations.AddField(
            model_name='imdbpopmovie',
            name='meta_url',
            field=models.CharField(default='#', max_length=500),
        ),
        migrations.AddField(
            model_name='imdbpopmovie',
            name='rotten_url',
            field=models.CharField(default='#', max_length=500),
        ),
        migrations.AddField(
            model_name='imdbpoptv',
            name='imdb_url',
            field=models.CharField(default='#', max_length=500),
        ),
        migrations.AddField(
            model_name='imdbpoptv',
            name='meta_url',
            field=models.CharField(default='#', max_length=500),
        ),
        migrations.AddField(
            model_name='imdbpoptv',
            name='rotten_url',
            field=models.CharField(default='#', max_length=500),
        ),
        migrations.AddField(
            model_name='imdbtopmovie',
            name='imdb_url',
            field=models.CharField(default='#', max_length=500),
        ),
        migrations.AddField(
            model_name='imdbtopmovie',
            name='meta_url',
            field=models.CharField(default='#', max_length=500),
        ),
        migrations.AddField(
            model_name='imdbtopmovie',
            name='rotten_url',
            field=models.CharField(default='#', max_length=500),
        ),
        migrations.AddField(
            model_name='imdbtoptv',
            name='imdb_url',
            field=models.CharField(default='#', max_length=500),
        ),
        migrations.AddField(
            model_name='imdbtoptv',
            name='meta_url',
            field=models.CharField(default='#', max_length=500),
        ),
        migrations.AddField(
            model_name='imdbtoptv',
            name='rotten_url',
            field=models.CharField(default='#', max_length=500),
        ),
    ]

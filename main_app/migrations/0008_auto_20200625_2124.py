# Generated by Django 3.0.7 on 2020-06-25 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0007_auto_20200624_0148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imdbpopularmovie',
            name='country',
            field=models.CharField(default='#', max_length=2000),
        ),
        migrations.AlterField(
            model_name='imdbpopularmovie',
            name='poster_link',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='imdbtopmovie',
            name='poster_link',
            field=models.CharField(max_length=1000),
        ),
    ]
# Generated by Django 3.0.7 on 2020-06-23 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0006_auto_20200623_2345'),
    ]

    operations = [
        migrations.AddField(
            model_name='imdbpopularmovie',
            name='country',
            field=models.CharField(default='#', max_length=500),
        ),
        migrations.AddField(
            model_name='imdbtopmovie',
            name='country',
            field=models.CharField(default='#', max_length=500),
        ),
    ]
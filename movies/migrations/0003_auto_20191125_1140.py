# Generated by Django 2.2.7 on 2019-11-25 02:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_actor'),
    ]

    operations = [
        migrations.RenameField(
            model_name='genre',
            old_name='genre_num',
            new_name='genreId',
        ),
        migrations.RenameField(
            model_name='genre',
            old_name='genre_name',
            new_name='name',
        ),
    ]

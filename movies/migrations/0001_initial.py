<<<<<<< HEAD
# Generated by Django 2.2.7 on 2019-11-25 07:17
=======
# Generated by Django 2.2.7 on 2019-11-25 07:18
>>>>>>> d606cff8c653d53cb39319b07c55ec99b074aa6d

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Actor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('gender', models.IntegerField()),
                ('images', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('original_title', models.TextField()),
                ('popularity', models.FloatField()),
                ('runtime', models.IntegerField()),
                ('release_date', models.DateField()),
                ('credit', models.TextField()),
                ('genres', models.TextField()),
            ],
        ),
    ]

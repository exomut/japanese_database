# Generated by Django 3.0.2 on 2020-01-20 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0004_auto_20200105_1721'),
    ]

    operations = [
        migrations.CreateModel(
            name='Example',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entry_id', models.IntegerField(default=0)),
                ('english', models.TextField(default='', verbose_name='English')),
                ('japanese', models.TextField(default='', verbose_name='Japanese')),
                ('break_down', models.TextField(default='', verbose_name='Japanese Break Down')),
            ],
        ),
    ]

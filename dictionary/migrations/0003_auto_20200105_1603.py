# Generated by Django 3.0.1 on 2020-01-05 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0002_auto_20200105_1547'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reading',
            name='re_restr',
            field=models.BooleanField(verbose_name='Reading Restrictions'),
        ),
    ]

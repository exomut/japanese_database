# Generated by Django 3.0.1 on 2020-01-04 01:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0002_auto_20200104_1014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reading',
            name='re_nokanji',
            field=models.TextField(null=True, verbose_name='No Kanji'),
        ),
    ]
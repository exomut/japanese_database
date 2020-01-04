# Generated by Django 3.0.1 on 2020-01-04 03:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0005_auto_20200104_1221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reading',
            name='re_nokanji',
            field=models.TextField(default='', verbose_name='No Kanji'),
        ),
        migrations.AlterField(
            model_name='translation',
            name='gloss',
            field=models.TextField(default='', verbose_name='Glossary'),
        ),
        migrations.AlterField(
            model_name='translation',
            name='lang',
            field=models.TextField(default='eng', verbose_name='Language'),
        ),
    ]

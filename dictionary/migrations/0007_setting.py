# Generated by Django 3.0.2 on 2020-01-20 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0006_auto_20200120_1742'),
    ]

    operations = [
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=128, verbose_name='Setting Name')),
                ('value', models.TextField(default='', verbose_name='Setting Value')),
            ],
        ),
    ]

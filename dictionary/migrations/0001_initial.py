# Generated by Django 3.0.1 on 2020-01-01 03:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Entries',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('japanese', models.CharField(max_length=1000)),
            ],
        ),
    ]

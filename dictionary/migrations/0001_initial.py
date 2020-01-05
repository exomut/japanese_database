# Generated by Django 3.0.1 on 2020-01-04 23:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ent_seq', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Translation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sense_num', models.IntegerField(default=0)),
                ('translation_num', models.IntegerField(default=0)),
                ('gloss', models.TextField(default='', verbose_name='Glossary')),
                ('lang', models.TextField(default='eng', verbose_name='Language')),
                ('g_gend', models.TextField(verbose_name='Gender')),
                ('g_type', models.TextField(verbose_name='Type')),
                ('entry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dictionary.Entry')),
            ],
        ),
        migrations.CreateModel(
            name='Sense',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sense_num', models.IntegerField(default=0)),
                ('stagk', models.TextField()),
                ('stagr', models.TextField()),
                ('xref', models.TextField(verbose_name='Cross Reference')),
                ('ant', models.TextField(verbose_name='Antonym')),
                ('pos', models.TextField(verbose_name='Part of Speech')),
                ('field', models.TextField()),
                ('misc', models.TextField(verbose_name='Miscellaneous')),
                ('lsource', models.TextField(verbose_name='Language Source')),
                ('dial', models.TextField(verbose_name='Dialect')),
                ('pri', models.TextField()),
                ('s_inf', models.TextField(verbose_name='Sense Information')),
                ('entry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dictionary.Entry')),
            ],
        ),
        migrations.CreateModel(
            name='Reading',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reading_num', models.IntegerField(default=0)),
                ('reb', models.TextField(verbose_name='Reading')),
                ('re_nokanji', models.TextField(default='', verbose_name='No Kanji')),
                ('re_restr', models.TextField(verbose_name='Reading Restrictions')),
                ('re_inf', models.TextField(verbose_name='Reading Information')),
                ('re_pri', models.TextField(verbose_name='Reading Priority')),
                ('entry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dictionary.Entry')),
            ],
        ),
        migrations.CreateModel(
            name='Kanji',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kanji_num', models.IntegerField(default=0)),
                ('keb', models.TextField(verbose_name='Kanji')),
                ('ke_inf', models.TextField(verbose_name='Kanji Information')),
                ('ke_pre', models.TextField(verbose_name='Kanji Priority')),
                ('entry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dictionary.Entry')),
            ],
        ),
    ]

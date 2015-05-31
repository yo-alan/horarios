# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Calendario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('curso', models.CharField(max_length=100, blank=True)),
                ('puntaje', models.IntegerField(default=0)),
                ('ranking_distribucion', models.FloatField(default=100)),
            ],
        ),
        migrations.CreateModel(
            name='Espacio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Horario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hora_desde', models.TimeField(verbose_name=b'desde', blank=True)),
                ('hora_hasta', models.TimeField(verbose_name=b'hasta', blank=True)),
                ('dia_semana', models.IntegerField(default=0, blank=True)),
                ('id_calendario', models.ForeignKey(to='calendario.Calendario')),
            ],
        ),
        migrations.CreateModel(
            name='Profesional',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=100, blank=True)),
                ('apellido', models.CharField(max_length=100, blank=True)),
                ('documento', models.IntegerField(default=0, blank=True)),
                ('especialidad', models.CharField(max_length=100, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Restriccion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hora_desde', models.TimeField(verbose_name=b'desde', blank=True)),
                ('hora_hasta', models.TimeField(verbose_name=b'hasta', blank=True)),
                ('dia_semana', models.IntegerField(default=0, blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='horario',
            name='id_profesional',
            field=models.ForeignKey(to='calendario.Profesional', blank=True),
        ),
    ]

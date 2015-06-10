# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calendario', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profesional',
            name='cuil',
            field=models.CharField(max_length=11, blank=True),
        ),
    ]

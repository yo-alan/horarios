# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calendario', '0002_auto_20150607_1944'),
    ]

    operations = [
        migrations.RenameField(
            model_name='calendario',
            old_name='curso',
            new_name='nombre',
        ),
    ]

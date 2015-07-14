# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('knowledge', '0005_auto_20150710_1146'),
    ]

    operations = [
        migrations.AddField(
            model_name='atomtype',
            name='bootstrap_label',
            field=models.CharField(max_length=30, default='default'),
        ),
    ]

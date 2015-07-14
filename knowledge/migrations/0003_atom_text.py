# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('knowledge', '0002_auto_20150705_1454'),
    ]

    operations = [
        migrations.AddField(
            model_name='atom',
            name='text',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]

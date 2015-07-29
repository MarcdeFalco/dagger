# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('knowledge', '0008_auto_20150716_1648'),
    ]

    operations = [
        migrations.AddField(
            model_name='atomtype',
            name='important',
            field=models.BooleanField(default=True),
        ),
    ]

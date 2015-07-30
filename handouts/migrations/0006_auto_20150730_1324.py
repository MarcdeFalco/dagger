# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('handouts', '0005_auto_20150712_1023'),
    ]

    operations = [
        migrations.AddField(
            model_name='paragraphcontainsatoms',
            name='lead_in',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='paragraphcontainsatoms',
            name='lead_out',
            field=models.TextField(blank=True),
        ),
    ]

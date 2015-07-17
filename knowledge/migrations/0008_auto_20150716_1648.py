# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import knowledge.db


class Migration(migrations.Migration):

    dependencies = [
        ('knowledge', '0007_auto_20150716_1647'),
    ]

    operations = [
        migrations.AlterField(
            model_name='atom',
            name='slug',
            field=knowledge.db.SlugOrNullField(max_length=60, null=True, unique=True, blank=True),
        ),
    ]

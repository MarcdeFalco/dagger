# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import knowledge.db


class Migration(migrations.Migration):

    dependencies = [
        ('knowledge', '0006_atomtype_bootstrap_label'),
    ]

    operations = [
        migrations.AlterField(
            model_name='atom',
            name='slug',
            field=knowledge.db.SlugOrNullField(blank=True, max_length=60, unique=True),
        ),
    ]

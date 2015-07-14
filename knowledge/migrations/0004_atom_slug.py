# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('knowledge', '0003_atom_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='atom',
            name='slug',
            field=models.SlugField(default='', max_length=60, unique=True),
            preserve_default=False,
        ),
    ]

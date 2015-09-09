# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('handouts', '0007_auto_20150909_0923'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='handout',
            options={'ordering': ['lead']},
        ),
        migrations.AlterModelOptions(
            name='paragraph',
            options={'ordering': ['name']},
        ),
    ]

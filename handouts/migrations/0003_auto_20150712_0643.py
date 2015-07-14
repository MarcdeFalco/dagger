# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('handouts', '0002_auto_20150712_0641'),
    ]

    operations = [
        migrations.AlterField(
            model_name='handout',
            name='lead',
            field=models.ForeignKey(to='handouts.Paragraph', related_name='handout_as_lead', blank=True),
        ),
    ]

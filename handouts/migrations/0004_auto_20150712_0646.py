# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('handouts', '0003_auto_20150712_0643'),
    ]

    operations = [
        migrations.AlterField(
            model_name='handout',
            name='lead',
            field=models.ForeignKey(null=True, to='handouts.Paragraph', blank=True, related_name='handout_as_lead'),
        ),
    ]

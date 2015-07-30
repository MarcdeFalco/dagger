# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('knowledge', '0009_atomtype_important'),
    ]

    operations = [
        migrations.AddField(
            model_name='atomrelationshiptype',
            name='fuse_into',
            field=models.BooleanField(default=False),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('handouts', '0006_auto_20150730_1324'),
    ]

    operations = [
        migrations.AddField(
            model_name='handout',
            name='cluster',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='handout',
            name='code',
            field=models.TextField(help_text='\nHandout code format :<br/>\n<br/>\nLead paragraph<br/>\n* Main paragraph<br/>\n** Sub paragraph<br/>\n<br/>\nIn each paragraph, you can reference atoms:<br/>\nDirect reference<br/>\n- atom_by_ref<br/>\nReference by relationships<br/>\n-> verb atom_by_ref [(all,random,first)]<br/>\nCreate a new atom and reference it<br/>\n-{ typ_slug [slug [name]]<br/>\nAtom text goes here<br/>\n}<br/>\n<br/>\nAfter each atom references you can add text: <br/>\ntext placed just before the atom to introduce it and can be multiline<br/>\n-- (optional separation and signal that )<br/>\nthe following lines are to be placed after the atom<br/>\n'),
        ),
    ]

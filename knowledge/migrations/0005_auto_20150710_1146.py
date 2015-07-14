# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('knowledge', '0004_atom_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='AtomOrphanRelationship',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('ref', models.SlugField(max_length=60)),
            ],
        ),
        migrations.AlterField(
            model_name='atom',
            name='slug',
            field=models.SlugField(unique=True, max_length=60, blank=True),
        ),
        migrations.AddField(
            model_name='atomorphanrelationship',
            name='atom',
            field=models.ForeignKey(to='knowledge.Atom'),
        ),
        migrations.AddField(
            model_name='atomorphanrelationship',
            name='typ',
            field=models.ForeignKey(to='knowledge.AtomRelationshipType'),
        ),
    ]

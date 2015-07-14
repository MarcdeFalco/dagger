# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Atom',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=200, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='AtomRelationship',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('from_atom', models.ForeignKey(related_name='from_atoms', to='knowledge.Atom')),
                ('to_atom', models.ForeignKey(related_name='to_atoms', to='knowledge.Atom')),
            ],
        ),
        migrations.CreateModel(
            name='AtomRelationshipType',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(max_length=30, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='AtomType',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(max_length=30, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='atomrelationship',
            name='typ',
            field=models.ForeignKey(to='knowledge.AtomRelationshipType'),
        ),
        migrations.AddField(
            model_name='atom',
            name='relationships',
            field=models.ManyToManyField(related_name='related_to', through='knowledge.AtomRelationship', to='knowledge.Atom'),
        ),
        migrations.AddField(
            model_name='atom',
            name='typ',
            field=models.ForeignKey(to='knowledge.AtomType'),
        ),
    ]

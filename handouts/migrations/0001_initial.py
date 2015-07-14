# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('knowledge', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Paragraph',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('slug', models.SlugField(max_length=100)),
                ('order', models.PositiveSmallIntegerField(default=1)),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('mptt_level', models.PositiveIntegerField(db_index=True, editable=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ParagraphContainsAtoms',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('order', models.PositiveSmallIntegerField(default=1)),
                ('atom', models.ForeignKey(to='knowledge.Atom')),
                ('paragraph', models.ForeignKey(to='handouts.Paragraph')),
            ],
        ),
        migrations.AddField(
            model_name='paragraph',
            name='content',
            field=models.ManyToManyField(through='handouts.ParagraphContainsAtoms', to='knowledge.Atom'),
        ),
        migrations.AddField(
            model_name='paragraph',
            name='parent',
            field=mptt.fields.TreeForeignKey(related_name='children', null=True, to='handouts.Paragraph', blank=True),
        ),
    ]

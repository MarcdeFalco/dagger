# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('handouts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Handout',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('code', models.TextField()),
                ('lead', models.ForeignKey(to='handouts.Paragraph', related_name='handout_as_lead')),
            ],
        ),
        migrations.AddField(
            model_name='paragraph',
            name='handout',
            field=models.ForeignKey(to='handouts.Handout', default=''),
            preserve_default=False,
        ),
    ]

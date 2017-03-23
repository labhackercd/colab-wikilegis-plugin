# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('colab_wikilegis', '0005_auto_20170317_2116'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wikilegiscomment',
            name='user',
        ),
        migrations.DeleteModel(
            name='WikilegisComment',
        ),
        migrations.RemoveField(
            model_name='wikilegissegment',
            name='author',
        ),
        migrations.RemoveField(
            model_name='wikilegissegment',
            name='bill',
        ),
        migrations.RemoveField(
            model_name='wikilegissegment',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='wikilegissegment',
            name='replaced',
        ),
        migrations.RemoveField(
            model_name='wikilegissegment',
            name='type',
        ),
        migrations.DeleteModel(
            name='WikilegisSegment',
        ),
        migrations.DeleteModel(
            name='WikilegisSegmentType',
        ),
    ]

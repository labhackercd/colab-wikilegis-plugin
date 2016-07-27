# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('colab_wikilegis', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wikilegisbill',
            name='created',
            field=models.DateTimeField(editable=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='wikilegisbill',
            name='modified',
            field=models.DateTimeField(editable=False),
            preserve_default=True,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('colab_wikilegis', '0004_wikilegisbill_closing_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='WikilegisBillTheme',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('description', models.CharField(unique=True, max_length=50)),
                ('slug', models.SlugField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='wikilegisbill',
            name='amendments_count',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='wikilegisbill',
            name='comments_count',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='wikilegisbill',
            name='downvote_count',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='wikilegisbill',
            name='upvote_count',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='wikilegisbill',
            name='votes_count',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='wikilegisbill',
            name='theme',
            field=models.ForeignKey(to='colab_wikilegis.WikilegisBillTheme'),
            preserve_default=True,
        ),
    ]

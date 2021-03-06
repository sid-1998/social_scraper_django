# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-19 18:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='quora',
            name='answers',
            field=models.CharField(blank=True, default='', max_length=30),
        ),
        migrations.AddField(
            model_name='quora',
            name='monthViews',
            field=models.CharField(blank=True, default='', max_length=30),
        ),
        migrations.AddField(
            model_name='quora',
            name='name',
            field=models.CharField(blank=True, default='', max_length=30),
        ),
        migrations.AddField(
            model_name='quora',
            name='totalViews',
            field=models.CharField(blank=True, default='', max_length=30),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-21 19:23
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20170419_1833'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='modeluser',
            name='user',
        ),
        migrations.DeleteModel(
            name='ModelUser',
        ),
    ]
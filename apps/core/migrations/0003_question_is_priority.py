# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-11 16:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20170706_1504'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='is_priority',
            field=models.BooleanField(default=False, verbose_name='is priority'),
        ),
    ]

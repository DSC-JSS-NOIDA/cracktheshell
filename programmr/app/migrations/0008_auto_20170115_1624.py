# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-15 10:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20170115_1601'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='total_score',
            field=models.IntegerField(default=0),
        ),
    ]
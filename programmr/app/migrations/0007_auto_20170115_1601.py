# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-15 10:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20170115_1537'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='total_submissions',
            field=models.CharField(default=b'0', max_length=10),
        ),
    ]

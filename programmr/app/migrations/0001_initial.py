# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-04 14:13
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='GoogleProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('google_user_id', models.CharField(max_length=100)),
                ('access_token', models.CharField(max_length=100)),
                ('profile_url', models.CharField(max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('detail', models.TextField()),
                ('constraint', models.CharField(max_length=120)),
                ('input_format', models.TextField()),
                ('output_format', models.TextField()),
                ('sample_testcase', models.TextField()),
                ('testcase_input', models.TextField()),
                ('testcase_output', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_ID', models.CharField(max_length=120)),
                ('question_ID', models.CharField(max_length=120)),
                ('status', models.CharField(max_length=120)),
                ('source_code_URL', models.URLField(max_length=120)),
                ('date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('email_ID', models.EmailField(blank=True, max_length=200)),
                ('avatar', models.URLField(max_length=120)),
                ('year', models.CharField(blank=True, max_length=120)),
                ('branch', models.CharField(blank=True, max_length=120)),
                ('mobile_no', models.CharField(blank=True, max_length=120)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('total_score', models.CharField(max_length=120)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

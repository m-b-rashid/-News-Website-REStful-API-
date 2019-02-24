# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-11-20 16:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('articleid', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=64)),
                ('content', models.TextField()),
                ('author', models.CharField(max_length=64)),
                ('postTime', models.DateTimeField()),
            ],
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-10 08:02
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('articles', '0012_auto_20171210_0243'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='dislikes',
            field=models.ManyToManyField(blank=True, related_name='post_dislikes', to=settings.AUTH_USER_MODEL),
        ),
    ]

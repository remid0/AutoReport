# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-09 09:22
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auto_report', '0006_auto_20171108_1536'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='is_autorized_to_change_mode',
            new_name='is_authorised_to_change_mode',
        ),
        migrations.RemoveField(
            model_name='gpspoint',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='gpspoint',
            name='updated_at',
        ),
    ]
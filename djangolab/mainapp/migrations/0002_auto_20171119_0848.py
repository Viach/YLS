# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-19 08:48
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lab',
            old_name='jsonfield',
            new_name='json_field',
        ),
    ]
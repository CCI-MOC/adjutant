# -*- coding: utf-8 -*-
# Generated by Django 1.11.21 on 2019-06-10 02:09
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20160929_0317'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.AlterModelTable(
                    name='task',
                    table='tasks_task',
                ),
            ],
        ),
    ]
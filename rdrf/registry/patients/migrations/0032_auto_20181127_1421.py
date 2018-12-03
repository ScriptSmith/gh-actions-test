# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-11-27 14:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0031_auto_20181123_1221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clinicianother',
            name='speciality',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='patients.Speciality'),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-04 00:04
from __future__ import unicode_literals

from django.db import migrations
from app.models import State
import csv

class Migration(migrations.Migration):

    def add_states(apps, schema_editor):
        State = apps.get_model("app", "State")
        with open("state_codes.csv", encoding="latin1") as infile:
            read_file = csv.reader(infile, delimiter=',')
            for row in read_file:
                State.objects.create(state_name=row[3])

    dependencies = [
        ('app', '0002_auto_20160803_2351'),
    ]

    operations = [
    migrations.RunPython(add_states)
    ]

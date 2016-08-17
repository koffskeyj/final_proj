from __future__ import unicode_literals

from django.db import migrations
from app.models import BasketballTeam, FootballTeam
import csv


class Migration(migrations.Migration):

    def add_football_teams(apps, schema_editor):
        FootballTeam = apps.get_model("app", "FootballTeam")
        with open("division_1_football.csv", encoding="latin1") as infile:
            read_file = csv.reader(infile, delimiter=',')
            for row in read_file:
                FootballTeam.objects.create(school=row[1], name=row[2])

    def add_basketball_teams(apps, schema_editor):
        BasketballTeam = apps.get_model("app", "BasketballTeam")
        with open("division_1_basketball.csv", encoding="latin1") as infile:
            read_file = csv.reader(infile, delimiter=',', quotechar='"')
            for row in read_file:
                BasketballTeam.objects.create(school=row[2], name=row[3])

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_basketball_teams),
        migrations.RunPython(add_football_teams)
    ]

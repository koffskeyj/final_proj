from django.contrib import admin
from django.db import models
from app.models import FootballTeam, BasketballTeam, Location, Profile, CheckIn, State

admin.site.register(FootballTeam)
admin.site.register(BasketballTeam)
admin.site.register(Location)
admin.site.register(Profile)
admin.site.register(CheckIn)
admin.site.register(State)

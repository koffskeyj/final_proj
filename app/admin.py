from django.contrib import admin
from app.models import FootballTeam, BasketballTeam, Location, Profile, CheckIn

admin.site.register(FootballTeam)
admin.site.register(BasketballTeam)
admin.site.register(Location)
admin.site.register(Profile)
admin.site.register(CheckIn)

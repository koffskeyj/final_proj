from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from geoposition.fields import GeopositionField
from django.forms import ModelForm

BASKETBALL = 'Basketball'
FOOTBALL = 'Football'
SPORT_CHOICES = ((BASKETBALL, 'Basketball'), (FOOTBALL, 'Football'))

class BasketballTeam(models.Model):
    school = models.CharField(max_length=30)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.school

    class Meta:
        ordering = ["school"]

class FootballTeam(models.Model):
    school = models.CharField(max_length=30)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.school

    class Meta:
        ordering = ["school"]


class State(models.Model):
    state_name = models.CharField(max_length=2)

    def __str__(self):
        return self.state_name


class Profile(models.Model):
    user = models.OneToOneField(User)
    bio = models.TextField(null=True, blank=True)
    basketball = models.ForeignKey(BasketballTeam, null=True, blank=True)
    football = models.ForeignKey(FootballTeam, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    state = models.ForeignKey(State, null=True, blank=True)
    zipcode = models.CharField(max_length=10, null=True, blank=True)
    photo = models.ImageField(upload_to="profile_photos", null=True, blank=True, verbose_name="Profile Photo")

    @property
    def photo_url(self):
        if self.photo:
            return self.photo.url
        return "http://www.sessionlogs.com/media/icons/defaultIcon.png"


class Location(models.Model):
    location_name = models.CharField(max_length=50, null=True, blank=True)
    location_city = models.CharField(max_length=50, null=True, blank=True)
    location_address = models.CharField(max_length=50, null=True, blank=True)
    location_zip = models.CharField(max_length=10, null=True, blank=True)
    geolocation = GeopositionField(null=True, blank=True)


class CheckIn(models.Model):
    checkin_user = models.ForeignKey(User)
    checkin_location = models.ForeignKey(Location)
    checkin_type = models.CharField(max_length=30, choices=SPORT_CHOICES, default=FOOTBALL)
    created = models.DateTimeField(auto_now_add=True)
    body = models.CharField(max_length=200, null=True, blank=True)



@receiver(post_save, sender="auth.User")
def create_user_profile(**kwargs):
    created = kwargs.get("created")
    instance = kwargs.get("instance")

    if created:
        Profile.objects.create(user=instance)

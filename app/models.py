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
    prof_user = models.OneToOneField(User)
    bio = models.TextField(null=True, blank=True)
    basketball = models.ForeignKey(BasketballTeam, null=True, blank=True)
    football = models.ForeignKey(FootballTeam, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    state = models.ForeignKey(State, null=True, blank=True)
    zipcode = models.CharField(max_length=10, null=True, blank=True)
    photo = models.ImageField(upload_to="profile_photos", null=True, blank=True, verbose_name="Profile Photo")

    def __str__(self):
        return self.prof_user.username


    @property
    def photo_url(self):
        if self.photo:
            return self.photo.url
        return "http://www.hi-wallpapers.com/uploads/image/201307/12/1373597280.jpg"


class Location(models.Model):
    location_name = models.CharField(max_length=50, null=True, blank=True)
    location_city = models.CharField(max_length=50, null=True, blank=True)
    location_address = models.CharField(max_length=50, null=True, blank=True)
    location_zip = models.CharField(max_length=10, null=True, blank=True)
    geolocation = GeopositionField(null=True, blank=True)

    class Meta:
        ordering = ["location_name"]

    def __str__(self):
        return self.location_name


class CheckIn(models.Model):
    checkin_user = models.ForeignKey(User)
    checkin_location = models.ForeignKey(Location)
    checkin_type = models.CharField(max_length=30, choices=SPORT_CHOICES, default=FOOTBALL)
    created = models.DateTimeField(auto_now_add=True)
    body = models.TextField(max_length=50, null=True, blank=True)


class Debate(models.Model):
    debate_user = models.ForeignKey(User)
    debate_location = models.ForeignKey(Location)
    body = models.TextField(max_length=100, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created"]


class DebateForm(ModelForm):

    class Meta:
        model = Debate
        fields = ["body"]


@receiver(post_save, sender="auth.User")
def create_user_profile(**kwargs):
    created = kwargs.get("created")
    instance = kwargs.get("instance")

    if created:
        Profile.objects.create(prof_user=instance)

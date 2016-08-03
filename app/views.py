from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import UpdateView, CreateView, FormView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.db.models import Count
from app.models import Location, CheckIn, FootballTeam, BasketballTeam, Debate, DebateForm
from app.forms import ChoosePlaceForm
from googleplaces import GooglePlaces, types, lang
from geoposition import Geoposition
from datetime import datetime, timedelta
from urllib.request import urlopen
import json
import requests
import os
YOUR_API_KEY = os.environ["places_key"]
google_places = GooglePlaces(YOUR_API_KEY)
ZIPCODE_API_KEY = os.environ["zipcodes_key"]

class IndexView(TemplateView):
    template_name = "index.html"


class UserCreateView(CreateView):
    model = User
    form_class = UserCreationForm
    success_url = "/login"


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    success_url = reverse_lazy("profile_update_view")
    fields = ["bio", "photo", "basketball", "football", "city", "state", "zipcode"]

    def get_object(self, queryset=None):
        return self.request.user.profile


def get_places_view(request):
    form = ChoosePlaceForm()
    if request.POST:
        form = ChoosePlaceForm(request.POST)
        if form.is_valid():
            location_name = form.cleaned_data['location_name']
            location_city = form.cleaned_data['location_city']
            #instance = form.save(commit=False)
            #instance.user = request.user
            #instance.save()
            if location_name != '':
                query_result = google_places.text_search(
                query=location_name, location=location_city,
                radius=20000,)
            list_of_places = []
            list_of_addresses = []
            list_of_geolocations = []
            locations = []
            for place in query_result.places:
                details = place.get_details()
                list_of_geolocations.append(place.geo_location)
                list_of_addresses.append((place.formatted_address, place.geo_location))
                list_of_places.append(place.name)

            return render(request, 'choose_place.html', {'geolocations' : list_of_geolocations, 'location' : location_city, 'addresses' : list_of_addresses, 'places' : list_of_places, 'form' : form})
    else:
        return render(request, 'choose_place.html', {'form': form})


class CheckInCreateView(LoginRequiredMixin, CreateView):
    model = CheckIn
    fields = ["checkin_type", "body"]
    success_url = "/"

    def get_context_data(self, **kwargs):
        from geoposition import Geoposition

        context = super().get_context_data()
        lat = self.request.GET.get("lat")
        lng = self.request.GET.get("lng")
        context["name"] = self.request.GET.get("name")
        context["address"] = self.request.GET.get("address")

        # context["form"].fields["checkin_location"].initial = Geoposition(lat, lng)
        return context

    def form_valid(self, form):
        checkin = form.save(commit=False)
        checkin.checkin_user = self.request.user
        lat = self.request.GET.get("lat")
        lng = self.request.GET.get("lng")
        name = self.request.GET.get("name")
        city = self.request.GET.get("city")
        address = self.request.GET.get("address")
        zip_address = self.request.GET.get("address").split(",")
        print(zip_address)
        zipcode = zip_address[2][4:10]
        print(zipcode)
        checkin.checkin_location, _ = Location.objects.get_or_create(location_name=name, location_address=address, location_zip=zipcode, geolocation=Geoposition(lat,lng))
        #checkin.save()
        return super().form_valid(form)


class FootballLocationListView(ListView):
    template_name = "app/football_location_list.html"

    def get_queryset(self):
        nearby_zips = []
        url = urlopen("https://www.zipcodeapi.com/rest/" + ZIPCODE_API_KEY + "/radius.json/{}/30/mile".format(self.request.user.profile.zipcode)).read()
        results = json.loads(url.decode())
        for item in results["zip_codes"]:
            nearby_zips.append(item["zip_code"])
        return Location.objects.filter(location_zip__in=nearby_zips).filter(checkin__checkin_user__profile__football=self.request.user.profile.football).filter(checkin__checkin_type="Football").distinct()

class BasketballLocationListView(ListView):
    template_name = "app/basketball_location_list.html"

    def get_queryset(self):
        nearby_zips = []
        url = urlopen("https://www.zipcodeapi.com/rest/" + ZIPCODE_API_KEY + "/radius.json/{}/30/mile".format(self.request.user.profile.zipcode)).read()
        results = json.loads(url.decode())
        for item in results["zip_codes"]:
            nearby_zips.append(item["zip_code"])
        return Location.objects.filter(checkin__checkin_user__profile__basketball=self.request.user.profile.basketball).filter(location_zip__in=nearby_zips).filter(checkin__checkin_type="Basketball").distinct()



class FootballCheckInListView(CreateView):
    model = CheckIn
    form_class = DebateForm
    template_name = "app/football_checkin_list.html"
    success_url = reverse_lazy("football_checkin_list_view")

    def form_valid(self, form, **kwargs):
        location = self.kwargs.get('pk', None)
        debate_body = form.cleaned_data["body"].lower()
        debate = form.save(commit=False)
        debate.debate_user = self.request.user
        debate.debate_location = Location.objects.get(id=location)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        location = self.kwargs.get('pk', None)
        location_debate = CheckIn.objects.get(checkin_location_id=location)
        teams = FootballTeam.objects.filter(pk__in=set(self.get_queryset().values_list("checkin_user__profile__football", flat=True)))
        users_pk = self.get_queryset().values_list("checkin_user__pk", flat=True).distinct()
        context["teams"] = FootballTeam.objects.filter(pk__in=set(self.get_queryset().values_list("checkin_user__profile__football", flat=True)))
        context["users_pk"] = self.get_queryset().values_list("checkin_user__pk", flat=True)
        context["location"] = Location.objects.get(id=location)
        context["debates"] = Debate.objects.filter(debate_location_id=location)
        context["object_list"] = self.get_queryset()
        # hellooooooo
        return context




class BasketballCheckInListView(CreateView):
    model = CheckIn
    template_name= "app/basketball_checkin_list.html"
    success_url = reverse_lazy("basketball_checkin_list_view")


    def form_valid(self,form):
        checkin_body = form.cleaned_data["body"].lower()
        checkin = form.save(commit=False)
        checkin.checkin_user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        teams_list = []
        users_list = []
        context = super().get_context_data(**kwargs)
        location = self.kwargs.get('pk', None)
        teams = BasketballTeam.objects.filter(pk__in=set(self.get_queryset().values_list("checkin_user__profile__basketball", flat=True)))
        users_pk = self.get_queryset().values_list("checkin_user__pk", flat=True).distinct()
        context["teams"] = BasketballTeam.objects.filter(pk__in=set(self.get_queryset().values_list("checkin_user__profile__basketball", flat=True)))
        context["users_pk"] = self.get_queryset().values_list("checkin_user__pk", flat=True)
        context["location"] = Location.objects.get(id=location)
        context["comment_list"] = CheckIn.objects.filter(checkin_location_id=location)
        context["object_list"] = self.get_queryset()

    def get_queryset(self):
        days_amount = 1
        location = self.kwargs.get('pk', None)
        return CheckIn.objects.filter(checkin_location_id=location)


class FootballCheckInDetailsListView(ListView):
    model = CheckIn
    template_name = "app/football_checkindetails_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["users"] = self.get_queryset().values_list("checkin_user__username", flat=True).distinct()
        context["user_count"] = self.get_queryset().values_list("checkin_user__username", flat=True).distinct().count()

        return context

    def get_queryset(self):
        location = self.kwargs.get('pk', None)
        team = self.request.GET.get("team")
        return CheckIn.objects.filter(checkin_location_id=location, checkin_user__profile__football__school=team)


class BasketballCheckInDetailsListView(ListView):
    model = CheckIn
    template_name = "app/basketball_checkindetails_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["users"] = self.get_queryset().values_list("checkin_user__username", flat=True).distinct()
        context["user_count"] = self.get_queryset().values_list("checkin_user__username", flat=True).distinct().count()
        return context

    def get_queryset(self):
        location = self.kwargs.get('pk', None)
        team = self.request.GET.get("team")
        return CheckIn.objects.filter(checkin_location_id=location, checkin_user__profile__basketball__school=team)

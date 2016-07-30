from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import UpdateView, CreateView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.db.models import Count
from app.models import Location, CheckIn, FootballTeam
from app.forms import ChoosePlaceForm
from googleplaces import GooglePlaces, types, lang
from geoposition import Geoposition
import os
YOUR_API_KEY = os.environ["places_key"]
google_places = GooglePlaces(YOUR_API_KEY)

class IndexView(TemplateView):
    template_name = "index.html"


class UserCreateView(CreateView):
    model = User
    form_class = UserCreationForm
    success_url = "/login"

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    success_url = reverse_lazy("profile_update_view")
    fields = ["bio", "basketball", "football", "city", "state"]

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
    fields = []
    success_url = "/hot_spots"

    def get_context_data(self, **kwargs):
        from geoposition import Geoposition

        context = super().get_context_data()
        lat = self.request.GET.get("lat")
        lng = self.request.GET.get("lng")

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
        print(address)
        checkin.checkin_location, _ = Location.objects.get_or_create(location_name=name, location_address=address, geolocation=Geoposition(lat,lng))
        #checkin.save()
        return super().form_valid(form)

class LocationListView(ListView):

    def get_context_data(self):
        context = super().get_context_data()
        context["lat"] = self.request.GET.get("lat")
        return context

    def get_queryset(self):
        return Location.objects.filter(checkin__checkin_user__profile__basketball=self.request.user.profile.basketball).filter(checkin__checkin_user__profile__football=self.request.user.profile.football).distinct()

class CheckInListView(ListView):
    model = CheckIn
    template_name= "app/checkin_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        location = self.kwargs.get('pk', None)
        # context["teams"] = FootballTeam.objects.all().profile_set.filter()
        context["teams"] = FootballTeam.objects.filter(pk__in=set(self.get_queryset().values_list("checkin_user__profile__football", flat=True)))
        context["users_pk"] = self.get_queryset().values_list("checkin_user__pk", flat=True)
        context["location"] = Location.objects.get(id=location)

        print(context["users_pk"]) # bringing back id of checkin
        return context

    def get_queryset(self):
        location = self.kwargs.get('pk', None)
        return CheckIn.objects.filter(checkin_location_id=location)


class CheckInDetailsListView(ListView):
    model = CheckIn
    template_name = "app/checkindetails_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["users"] = self.get_queryset().values_list("checkin_user__username", flat=True).distinct()
        return context

    def get_queryset(self):
        location = self.kwargs.get('pk', None)
        team = self.request.GET.get("team")
        return CheckIn.objects.filter(checkin_location_id=location, checkin_user__profile__football__school=team)

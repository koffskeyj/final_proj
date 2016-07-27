from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import UpdateView, CreateView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from app.models import Location
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
    fields = ["bio", "basketball", "football"]

    def get_object(self, queryset=None):
        return self.request.user.profile

def get_places_view(request):
    form = ChoosePlaceForm()
    if request.POST:
        form = ChoosePlaceForm(request.POST)
        if form.is_valid():
            location_name = form.cleaned_data['location_name']
            location_city = form.cleaned_data['location_city']
            # instance = form.save(commit=False)
            # instance.user = request.user
            # instance.save()
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
    model = Location
    fields = ["location"]
    success_url = "/choose_place"

    def get_context_data(self):
        from geoposition import Geoposition

        context = super().get_context_data()
        lat = self.request.GET.get("lat")
        lng = self.request.GET.get("lng")

        context["form"].fields["location"].initial = Geoposition(lat, lng)
        return context

    def form_valid(self, form):
        place = form.save(commit=False)
        place.location_name = self.request.GET.get("name")
        place.location_city = self.request.GET.get("city")
        place.user = self.request.user
        return super().form_valid(form)

class CheckInListView(ListView):
    def get_queryset(self):
        return Location.objects.filter(user__profile__basketball=self.request.user.profile.basketball).filter(user__profile__football=self.request.user.profile.football)

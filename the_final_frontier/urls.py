"""the_final_frontier URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from app.views import IndexView, UserCreateView, ProfileUpdateView, CheckInCreateView, FootballLocationListView, BasketballLocationListView, FootballCheckInListView, BasketballCheckInListView, FootballCheckInDetailsListView, BasketballCheckInDetailsListView, get_places_view

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^$', IndexView.as_view(), name="index_view"),
    url(r'^user_create/$', UserCreateView.as_view(), name='user_create_view'),
    url(r'^accounts/profile/$', ProfileUpdateView.as_view(), name='profile_update_view'),
    url(r'^choose_place/$', get_places_view, name='get_places_view'),
    url(r'^checkin/$', CheckInCreateView.as_view(), name='check_in_create_view'),
    url(r'^football_hot_spots/$', FootballLocationListView.as_view(), name='football_location_list_view'),
    url(r'^basketball_hot_spots/$', BasketballLocationListView.as_view(), name="basketball_location_list_view"),
    url(r'^football_location/(?P<pk>\d+)/checkins/$', FootballCheckInListView.as_view(), name='football_checkin_list_view'),
    url(r'^basketball_location/(?P<pk>\d+)/checkins/$', BasketballCheckInListView.as_view(), name='basketball_checkin_list_view'),
    url(r'^football_location/(?P<pk>\d+)/checkins/checkin_details/$', FootballCheckInDetailsListView.as_view(), name='football_checkin_details_list_view'),
    url(r'^basketball_location/(?P<pk>\d+)/checkins/checkin_details/$', BasketballCheckInDetailsListView.as_view(), name='football_checkin_details_list_view'),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

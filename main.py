import requests
import json
from bs4 import BeautifulSoup

from googleplaces import GooglePlaces, types, lang

YOUR_API_KEY = "AIzaSyByCXfqVTQhBbbZYmmfNUeVs3NLg1AxCUc"

google_places = GooglePlaces(YOUR_API_KEY)

def get_places():
    # location_name = self.kwargs['location_name']
    # if location_name != '':
    query_result = google_places.text_search(location='29607',
        query='carolina ale house',)

    if query_result.has_attributions:
        print(query_result.html_attributions)


    for place in query_result.places:
        place.get_details()
        print(place.formatted_address)

get_places()

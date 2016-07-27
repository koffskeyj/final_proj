from django import forms
from app.models import Location

class ChoosePlaceForm(forms.ModelForm):
    class Meta:
        model = Location
        widgets = {
            'location_name': forms.TextInput(attrs={'placeholder' : 'Enter Name of Place...'}),
            'location_city': forms.TextInput(attrs={'placeholder' : 'Enter City/State or Zip'}),
        }
        fields = ["location_name", "location_city"]

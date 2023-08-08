from logging import PlaceHolder
from django import forms
from django.forms import ModelForm
from .models import Venue


# Create a Venue forms
class VenueForm(ModelForm):
    class Meta:
        model = Venue
        fields = (
            "name",
            "address",
            "zip_code",
            "phone",
            "web",
            "email_address",
        )
        labels = {
            "name": "",
            "address": "",
            "zip_code": "",
            "phone": "",
            "web": "",
            "email_address": "",
        }
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Name of the venue"}
            ),
            "address": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Venue Address Here"}
            ),
            "zip_code": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Postcode"}
            ),
            "phone": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Phone Number"}
            ),
            "web": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Web Address"}
            ),
            "email_address": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Email Address for the Venue",
                }
            ),
        }

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from .models import User  # Import your custom User model

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User  # Ensure the form uses your custom User model
        fields = ['username', 'password1', 'password2', 'role']  # Add 'role' to the form fields

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Enter Username'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password'}))

# forms.py
from django import forms
from django import forms

# Define the choices for fields
STATUS_CHOICES = [
    ('Empty', 'Empty'),
    ('Full', 'Full'),
    ('Half Full', 'Half Full'),
]

BIN_TYPE_CHOICES = [
    ('Organic', 'Organic'),
    ('Plastic', 'Plastic'),
    ('Paper', 'Paper'),
    ('Metal', 'Metal'),
]

COLLECTION_FREQUENCY_CHOICES = [
    ('Daily', 'Daily'),
    ('Weekly', 'Weekly'),
    ('Bi-Weekly', 'Bi-Weekly'),
]

class BinForm(forms.Form):
    bin_id  = forms.IntegerField()
    location = forms.CharField(max_length=255)
    waste_level = forms.IntegerField()
    status = forms.ChoiceField(choices=STATUS_CHOICES)
    temperature = forms.FloatField()
    bin_type = forms.ChoiceField(choices=BIN_TYPE_CHOICES)
    capacity = forms.IntegerField()
    daily_average_waste = forms.FloatField()
    collection_frequency = forms.ChoiceField(choices=COLLECTION_FREQUENCY_CHOICES)
    latitude = forms.FloatField()
    longitude = forms.FloatField()


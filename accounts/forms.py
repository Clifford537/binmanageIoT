from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import PasswordChangeForm
from .models import User  # Import your custom User model

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User  # Ensure the form uses your custom User model
        fields = ['username', 'password1', 'password2', 'role']  # Add 'role' to the form fields

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Enter Username'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password'}))
from django import forms

class BinForm(forms.Form):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]
    BIN_TYPE_CHOICES = [
        ('organic', 'Organic'),
        ('recyclable', 'Recyclable'),
        ('general', 'General'),
    ]

    bin_id = forms.CharField(max_length=50)
    waste_level = forms.IntegerField()
    status = forms.ChoiceField(choices=STATUS_CHOICES)
    temperature = forms.FloatField()
    bin_type = forms.ChoiceField(choices=BIN_TYPE_CHOICES)
    capacity = forms.IntegerField()
    daily_average_waste = forms.FloatField()
    collection_frequency = forms.IntegerField()
    latitude = forms.CharField(max_length=100, required=False)
    longitude = forms.CharField(max_length=100, required=False)
    location = forms.CharField(max_length=255, required=False)



class CustomPasswordChangeForm(PasswordChangeForm):
    # You can customize fields or validation here if needed
    old_password = forms.CharField(widget=forms.PasswordInput, label="Old Password")
    new_password1 = forms.CharField(widget=forms.PasswordInput, label="New Password")
    new_password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm New Password")

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

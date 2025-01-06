from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import User
from .forms import LoginForm 
from django.contrib import messages

def home_page(request):
    return render(request, 'accounts/home.html')

 # Assuming you have a LoginForm

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.role == 'admin':
                return redirect('admin_dashboard')  # Replace with your admin dashboard URL name
            elif user.role == 'municipal_authority':
                return redirect('municipal_dashboard')  # Replace with your municipal dashboard URL name
        else:
            messages.error(request, 'Invalid credentials')

    return render(request, 'accounts/login.html')
from .forms import CustomUserCreationForm

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new user
            return redirect('login')  # Redirect to the login page or dashboard after registration
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})

def admin_dashboard(request):
    return render(request, 'accounts/admin_dashboard.html')

def municipal_dashboard(request):
    return render(request, 'accounts/municipal_dashboard.html')

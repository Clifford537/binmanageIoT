from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponse
from .models import User
from .forms import CustomUserCreationForm, BinForm
import os
import csv
import pandas as pd
import json



# Views for user management
def home_page(request):
    return render(request, 'accounts/home.html')

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

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new user
            return redirect('login')  # Redirect to the login page or dashboard after registration
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})


import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import os
import csv
from django.conf import settings

@login_required
def admin_dashboard(request):
    bins = []

    # Define the path to the CSV file
    csv_file_path = os.path.join(settings.BASE_DIR, 'data', 'waste_bins.csv')

    try:
        # Read and parse the CSV file
        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                bins.append({
                    "bin_id": row["bin_id"],
                    "latitude": row["latitude"],
                    "longitude": row["longitude"],
                    "location": row["location"],
                    "waste_level": row["waste_level"],
                    "status": row["status"],
                    "last_updated": row["last_updated"],
                    "temperature": row["temperature"],
                    "bin_type": row["bin_type"],
                    "capacity": row["capacity"],
                    "daily_average_waste": row["daily_average_waste"],
                    "collection_frequency": row["collection_frequency"]
                })

        # Success message
        messages.success(request, f"Successfully loaded {len(bins)} bins.")
    
    except FileNotFoundError:
        messages.error(request, "CSV file not found.")

    # Pass the bins as a JSON string
    return render(request, "accounts/admin_dashboard.html", {"bins": json.dumps(bins)})


@login_required
def municipal_dashboard(request):
    # Get the absolute path to the CSV file
    csv_file_path = os.path.join(settings.BASE_DIR, 'data', 'waste_bins.csv')

    # Load data into a Pandas DataFrame
    df = pd.read_csv(csv_file_path)

    # Convert relevant columns to numeric
    numeric_columns = ['temperature', 'waste_level', 'capacity']
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Drop rows with NaN in critical columns
    df = df.dropna(subset=numeric_columns)

    # Aggregated data
    status_count = df['status'].value_counts().to_dict()
    status_count = {key.replace(" ", "_"): value for key, value in status_count.items()}  # Replace spaces with underscores

    # Bin count by city
    bin_count_by_city = df['location'].apply(lambda x: x.split(",")[0]).value_counts().to_dict()

    # Material type analysis
    material_analysis = df['bin_type'].value_counts().to_dict()

    # Temperature statistics by status
    temp_analysis = df.groupby('status')['temperature'].agg(['mean', 'std']).reset_index().to_dict('records')

    # Collection frequency count
    collection_frequency_count = df['collection_frequency'].value_counts().to_dict()

    # Prepare context data
    context = {
        'bins': json.dumps(df.to_dict('records')),
        'status_count': json.dumps(status_count),
        'bin_count_by_city': json.dumps(bin_count_by_city),
        'material_analysis': json.dumps(material_analysis),
        'temp_analysis': json.dumps(temp_analysis),
        'collection_frequency_count': json.dumps(collection_frequency_count),
    }
    return render(request, 'accounts/municipal_dashboard.html', context)

# View for adding bin dataimport os

def add_bin(request):
    if request.method == "POST":
        form = BinForm(request.POST)
        if form.is_valid():
            # Get the data from the form
            bin_id = form.cleaned_data['bin_id']  # Get the bin_id directly
            location = form.cleaned_data['location']
            waste_level = form.cleaned_data['waste_level']
            status = form.cleaned_data['status']
            temperature = form.cleaned_data['temperature']
            bin_type = form.cleaned_data['bin_type']
            capacity = form.cleaned_data['capacity']
            daily_average_waste = form.cleaned_data['daily_average_waste']
            collection_frequency = form.cleaned_data['collection_frequency']
            latitude = form.cleaned_data['latitude']
            longitude = form.cleaned_data['longitude']

            # Get the absolute path to the CSV file
            csv_file_path = os.path.join(settings.BASE_DIR, 'data', 'waste_bins.csv')

            try:
                # Open the CSV file and append the data
                with open(csv_file_path, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([bin_id, location, waste_level, status, '2025-01-01 00:00:00', temperature, bin_type, capacity, daily_average_waste, collection_frequency, latitude, longitude])

                # Notify user that the data has been successfully added
                messages.success(request, "Bin data added successfully!")

                return HttpResponse("Bin data added successfully!")
            except Exception as e:
                messages.error(request, f"Error saving bin data: {str(e)}")
                return HttpResponse("There was an error saving the data. Please try again.")
    else:
        form = BinForm()

    return render(request, 'accounts/create_bin.html', {'form': form})


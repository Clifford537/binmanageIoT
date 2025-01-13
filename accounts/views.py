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
from django.contrib.auth import logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from datetime import datetime
from .forms import BinForm  
from django.db import IntegrityError
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .models import EmailNotification
from bs4 import BeautifulSoup

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
            try:
                form.save()  # Save the new user
                messages.success(request, "Your account has been created successfully!")
                return redirect('login')  # Redirect to the login page or dashboard after registration
            except IntegrityError:
                # Catch the error if the account already exists (e.g., duplicate username)
                form.add_error('username', 'A user with that username already exists.')
                messages.error(request, "An error occurred. Please check the form below.")
        else:
            # If form is not valid, display a general error message
            messages.error(request, "There were errors in your submission. Please check the form below.")
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()  # Save the new password
            update_session_auth_hash(request, form.user)  # Keep the user logged in
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')  # Redirect to a profile or desired page
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'accounts/change_password.html', {'form': form})

@login_required
def municipal_dashboard(request):
    # Get the absolute path to the CSV file
    csv_file_path = os.path.join(settings.BASE_DIR, 'data', 'waste_bins.csv')

    # Read the CSV file
    bins = []
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            bins.append(row)

    # Pass data to the template
    return render(request, 'accounts/admin_dashboard.html', {'bins': bins})

@login_required
def add_bin(request):
    csv_file_path = os.path.join(settings.BASE_DIR, 'data', 'waste_bins.csv')

    if request.method == 'POST':
        # Extract data from the form
        bin_id = request.POST.get('bin_id')
        waste_level = 0
        status = request.POST.get('status')
        temperature = request.POST.get('temperature')
        bin_type = request.POST.get('bin_type')
        capacity = request.POST.get('capacity')
        latitude = request.POST.get('latitude', '')
        longitude = request.POST.get('longitude', '')
        location = request.POST.get('location', '')

        # Default values for fields not in the form
        daily_average_waste = 0  # Set to 0
        collection_frequency = 0  # Set to 0
        contact = "cliffordmukosh@gmail.com"  # Hardcoded or dynamic
        last_updated = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Add timestamp

        # Save data to CSV
        try:
            # Ensure the 'data' directory exists
            os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)

            # Check if the file exists to write headers if needed
            file_exists = os.path.isfile(csv_file_path)

            with open(csv_file_path, 'a', newline='') as file:
                writer = csv.writer(file)

                # Write headers if the file is new
                if not file_exists:
                    writer.writerow([  # Define headers in the CSV
                        "bin_id", "location", "waste_level", "status", "last_updated",
                        "temperature", "bin_type", "capacity", "daily_average_waste",
                        "collection_frequency", "latitude", "longitude", "contact"
                    ])

                # Write the new bin data
                writer.writerow([  # Write data to CSV
                    bin_id, location, waste_level, status, last_updated,
                    temperature, bin_type, capacity, daily_average_waste,
                    collection_frequency, latitude, longitude, contact
                ])
            messages.success(request, "Bin data successfully saved!")
        except Exception as e:
            messages.error(request, f"Error saving data: {str(e)}")

        # Redirect to the municipal dashboard after saving
        return redirect('municipal_dashboard')

    # Instantiate the form if it's a GET request
    form = BinForm()

    return render(request, 'accounts/create_bin.html', {'form': form})  # Pass the form to the template


@login_required
def admin_dashboard(request):
    # Get the unread notifications count
    unread_notifications = EmailNotification.objects.filter(read=False).count()

    # Define the path to the CSV file
    csv_file_path = os.path.join(settings.BASE_DIR, 'data', 'waste_bins.csv')

    # Read the CSV file
    bins = []
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            bins.append(row)

    # Fetch the latest email notifications (limit to 5 most recent)
    notifications = EmailNotification.objects.all().order_by('-sent_at')[:5]

    # Pass data to the template
    return render(request, 'accounts/admin_dashboard.html', {
        'bins': bins,
        'unread_notifications': unread_notifications,
        'notifications': notifications
    })


@login_required
def delete_bin(request, bin_id):
    # Define the path to the CSV file
    csv_file_path = os.path.join(settings.BASE_DIR, 'data', 'waste_bins.csv')

    # Read the current CSV data
    bins = []
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        bins = [row for row in reader if row['bin_id'] != bin_id]  # Exclude the bin with the given bin_id

    # Write the updated data back to the CSV
    fieldnames = ['bin_id', 'location', 'waste_level', 'status', 'last_updated', 'temperature', 
                  'bin_type', 'capacity', 'daily_average_waste', 'collection_frequency', 'latitude', 
                  'longitude', 'contact']
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(bins)

    return redirect('admin_dashboard')


@login_required
def edit_bin(request, bin_id):
    # Define the path to the CSV file
    csv_file_path = os.path.join(settings.BASE_DIR, 'data', 'waste_bins.csv')

    # Read the current CSV data
    bins = []
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            bins.append(row)

    # Find the bin to edit
    bin_to_edit = next((bin for bin in bins if bin['bin_id'] == bin_id), None)
    if not bin_to_edit:
        return render(request, 'accounts/admin_dashboard.html', {'bins': bins, 'error': 'Bin not found'})

    if request.method == 'POST':
        # Update bin data from the form
        for key in bin_to_edit.keys():
            if key in request.POST:
                bin_to_edit[key] = request.POST[key]

        # Write the updated data back to the CSV
        fieldnames = ['bin_id', 'location', 'waste_level', 'status', 'last_updated', 'temperature', 
                      'bin_type', 'capacity', 'daily_average_waste', 'collection_frequency', 'latitude', 
                      'longitude', 'contact']
        with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(bins)

        return redirect('admin_dashboard')

    return render(request, 'accounts/edit_bin.html', {'bin': bin_to_edit})



def logout_view(request):
    logout(request)  # Logs the user out
    return redirect('login')

@login_required
def empty_bin(request, bin_id):
    csv_file_path = os.path.join(settings.BASE_DIR, 'data', 'waste_bins.csv')

    # Read and update the CSV data
    bins = []
    bin_emptied = False  # Flag to check if the bin was successfully emptied
    bin_already_empty = False  # Flag to check if the bin is already empty
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['bin_id'] == bin_id:
                if row['waste_level'] == '0':  # Check if the bin is already empty
                    bin_already_empty = True  # Set the flag to True if the bin is already empty
                else:
                    row['waste_level'] = '0'  # Set waste level to 0 when bin is emptied
                    # Increment the collection frequency by 1 (ensure it's an integer)
                    current_frequency = int(row['collection_frequency'])
                    row['collection_frequency'] = str(current_frequency + 1)
                    bin_emptied = True  # Set the flag to True when the bin is emptied
            bins.append(row)

    # Write the updated data back to the CSV
    fieldnames = ['bin_id', 'location', 'waste_level', 'status', 'last_updated', 'temperature', 
                  'bin_type', 'capacity', 'daily_average_waste', 'collection_frequency', 'latitude', 
                  'longitude', 'contact']
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(bins)

    # Add success or informational messages
    if bin_emptied:
        messages.success(request, f"Bin {bin_id} emptied successfully!")
    elif bin_already_empty:
        messages.info(request, f"Bin {bin_id} is already empty!")

    return redirect('admin_dashboard')
  # Import BeautifulSoup to parse and extract text from HTML

@login_required
def add_dust_to_bin(request, bin_id):
    csv_file_path = os.path.join(settings.BASE_DIR, 'data', 'waste_bins.csv')

    # Read and update the CSV data
    bins = []
    email_sent = False  # Track if an email is sent
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['bin_id'] == bin_id:
                current_level = int(row['waste_level'])
                max_capacity = int(row['capacity'])
                new_level = current_level + 10  # Increase waste level by 10

                # Check if the new waste level exceeds 80
                if new_level >= 80 and not email_sent:  # Send email notification
                    contact_email = row['contact']
                    bin_location = row['location']
                    bin_type = row['bin_type']

                    # Email content with HTML styling, using "Trash Nova" as the app name
                    subject = f"Trash Nova: Waste Bin {bin_id} Alert"
                    message_html = f"""
                    <html>
                        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                            <h2 style="color: #2e8b57;">Trash Nova</h2>
                            <p>Dear User,</p>
                            <p style="color: #00008b;">
                                The waste bin with ID <strong>{bin_id}</strong> located at 
                                <strong>{bin_location}</strong> (Type: <strong>{bin_type}</strong>) 
                                has reached a waste level of <strong>{new_level}</strong>.
                            </p>
                            <p style="color: #2e8b57;">
                                Please arrange for collection to avoid overflow and ensure a clean environment.
                            </p>
                            <p>Thank you for using <strong>Trash Nova</strong>.</p>
                            <p style="color: #00008b;"><strong>The Trash Nova Team</strong></p>
                        </body>
                    </html>
                    """
                    # Extract plain text from the HTML message using BeautifulSoup
                    soup = BeautifulSoup(message_html, 'html.parser')
                    message_text = soup.get_text()

                    # Send the email with HTML content
                    try:
                        send_mail(
                            subject,
                            message_text,  # Send the plain text version of the message
                            settings.DEFAULT_FROM_EMAIL,
                            [contact_email],
                            html_message=message_html  # Include HTML message
                        )
                        email_sent = True  # Mark email as sent

                        # Save email details to the database (save the plain text message)
                        EmailNotification.objects.create(
                            sender=settings.DEFAULT_FROM_EMAIL,
                            recipient=contact_email,
                            subject=subject,
                            message=message_text,  # Save the plain text version
                            sent_at=timezone.now(),
                            read=False  # Mark as unread
                        )
                    except Exception as e:
                        # Handle email sending failure (optional)
                        print(f"Error sending email: {e}")

                # Set the new waste level to the bin
                row['waste_level'] = str(new_level)

            bins.append(row)

    # Write the updated data back to the CSV
    fieldnames = [
        'bin_id', 'location', 'waste_level', 'status', 'last_updated', 'temperature', 
        'bin_type', 'capacity', 'daily_average_waste', 'collection_frequency', 'latitude', 
        'longitude', 'contact'
    ]
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(bins)

    return redirect('admin_dashboard')

@login_required
def mark_as_read(request, notification_id):
    try:
        notification = EmailNotification.objects.get(id=notification_id)
        notification.read = True
        notification.save()
    except EmailNotification.DoesNotExist:
        pass  # Handle the case where the notification doesn't exist
    return redirect('admin_dashboard')



@login_required
def delete_notification(request, notification_id):
    try:
        notification = EmailNotification.objects.get(id=notification_id)
        notification.delete()
    except EmailNotification.DoesNotExist:
        pass  # Handle the case where the notification doesn't exist
    return redirect('admin_dashboard')

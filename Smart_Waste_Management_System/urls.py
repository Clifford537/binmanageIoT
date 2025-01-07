"""
URL configuration for Smart_Waste_Management_System project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static 
from django.conf import settings
 # Add include to include accounts URLs

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Include URLs from the accounts app
    path('', include('accounts.urls')),  # Use '' for the home page

    # If you want to define other app URLs later, you can add them here
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

from django.urls import path
from . import views

urlpatterns = [
    # Main/Home page URL
    path('', views.home_page, name='home'),

    # Account-related URLs
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('municipal_dashboard/', views.municipal_dashboard, name='municipal_dashboard'),
]

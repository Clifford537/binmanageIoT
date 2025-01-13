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
    path('add-bin/', views.add_bin, name='add_bin'),
    path('delete_bin/<str:bin_id>/', views.delete_bin, name='delete_bin'),
    path('edit_bin/<str:bin_id>/', views.edit_bin, name='edit_bin'),
    path('empty_bin/<str:bin_id>/', views.empty_bin, name='empty_bin'),
    path('add_dust_to_bin/<str:bin_id>/', views.add_dust_to_bin, name='add_dust_to_bin'),
    path('logout/', views.logout_view, name='logout'),
    path('change-password/', views.change_password, name='change_password'),

    path('mark_as_read/<int:notification_id>/', views.mark_as_read, name='mark_as_read'),
    path('delete_notification/<int:notification_id>/', views.delete_notification, name='delete_notification'),
]

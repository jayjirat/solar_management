
from django.urls import path
from . import views

urlpatterns = [
    path('admin-system/users_management/', views.users_management, name='users_management'),
    path('admin-system/dashboard/', views.dashboard, name='dashboard'),
    path('admin-system/solar_management/', views.solar, name='solar_management'),
    path('admin-system/upload_history/', views.upload, name='upload_history'),
    path('admin-system/reports/', views.reports, name='reports'),
]

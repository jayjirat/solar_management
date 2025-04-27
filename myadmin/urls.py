
from django.urls import path
from . import views

urlpatterns = [
    path('users_management/', views.users_management, name='users_management'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('solar_management/', views.solar, name='solar_management'),
    path('upload_history/', views.upload, name='upload_history'),
    path('reports/', views.reports, name='reports'),
    path('profile/', views.profile, name='profile'),
]

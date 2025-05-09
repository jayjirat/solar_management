
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('users_management/', views.users_management, name='users_management'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('solar_management/', views.solar, name='solar_management'),
    path('upload_history/', views.upload, name='upload_history'),
    path('reports/', views.reports, name='reports'),
    path('profile/', views.profile, name='profile'),
    path('profile/update-name/', views.update_display_name, name='update_display_name'),
    path('profile/upload-image/', views.upload_profile_image, name='upload_profile_image'),
    path('solar_management/create/', views.create_powerplant, name='create'),
]

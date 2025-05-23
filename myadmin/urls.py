
from django.urls import path
from . import views

urlpatterns = [
    path('users_management/', views.users_management, name='users_management'),
    path('users_management/<int:user_id>', views.users_management_manage, name='users_management_manage'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('powerplant_management/', views.solar, name='powerplant_management'),
    path('upload_history/', views.upload, name='upload_history'),
    path('reports/', views.reports, name='reports'),
    path('reports/<int:report_id>', views.reports_detail, name='reports_detail'),
    path('profile/', views.profile, name='profile'),
    path('create_power_plant/', views.create_power_plant, name='create')
]

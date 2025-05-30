
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('users_management/', views.users_management, name='users_management'),
    path('users_management/<int:user_id>/', views.users_management_manage, name='users_management_manage'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('solar_management/', views.solar, name='solar_management'),
    path('solar_management/<int:powerplant_id>/', views.solar_manage, name='solar_management_manage'),
    path('upload_history/', views.upload, name='upload_history'),
    path('reports/', views.reports, name='reports'),
    path('profile/', views.profile, name='profile'),
    path('profile/update-name/', views.update_display_name, name='update_display_name'),
    path('profile/upload-image/', views.upload_profile_image, name='upload_profile_image'),
    path('solar_management/create/', views.create_powerplant, name='create'),
    path('report_detail/<int:report_id>/', views.report_detail, name='report_detail'),
    path('upload_history/', views.upload, name='upload_history'),
    path('get_zones/<int:powerplant_id>/', views.get_zones, name='get_zones'),
    path('report_upload/<int:report_id>', views.report_upload, name='report_upload'),
    path('create_report/', views.create_report, name='create_report')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

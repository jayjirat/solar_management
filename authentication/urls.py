from django.urls import path
from . import views
from .views import SendOTPView, VerifyOTPView

urlpatterns = [
    path('', views.home, name='home'), 
    path('api/register/', views.register, name='register'),
    path('api/get_users/', views.get_users, name='get_users'),
    path('signup/', views.signup, name='signup'),
    path("api/send-otp/", SendOTPView.as_view(), name="send-otp"),
    path("api/verify-otp/", VerifyOTPView.as_view(), name="verify-otp"),
    path("verify-account/", views.verify_account, name="verify-account"),
]

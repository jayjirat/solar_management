from django.urls import path
from . import views
from .views import ThammasatLoginAPI, tu_login_page
from .views import LoginView, login_view, LogoutView, SendOTPView, VerifyOTPView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('', views.home, name='home'),
    path('api/login/', LoginView.as_view(), name='api_login'),
    path('login/', login_view, name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/logout/', LogoutView.as_view(), name='api_logout'),
    path('api/register/', views.register, name='register'),
    path('api/get_users/', views.get_users, name='get_users'),
    path('signup/', views.signup, name='signup'),
    path("api/send-otp/", SendOTPView.as_view(), name="send-otp"),
    path("api/verify-otp/", VerifyOTPView.as_view(), name="verify-otp"),
    path("verify-account/", views.verify_account, name="verify-account"),
    path('login/google/', views.google_login, name='google_login'),
    path('login/google/callback/', views.google_callback, name='google_callback'),
    path('login/facebook/', views.facebook_login, name='facebook_login'),  
    path('login/facebook/callback/', views.facebook_callback, name='facebook_callback'),  
    path("api/login/tu/", ThammasatLoginAPI.as_view(), name="tu-login"),
    path("login/tu/", tu_login_page, name="tu-login-page"),
]

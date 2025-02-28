from django.urls import path
from . import views
from .views import LoginView, login_view, LogoutView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('', views.home, name='home'),
    path('api/login/', LoginView.as_view(), name='api_login'),
    path('login/', login_view, name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/logout/', LogoutView.as_view(), name='api_logout'),
]

from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('login/google/', views.google_login, name='google_login'),
    path('login/google/callback/', views.google_callback, name='google_callback'),
    path('login/facebook/', views.facebook_login, name='facebook_login'),  # Add this line
    path('login/facebook/callback/', views.facebook_callback, name='facebook_callback'),  # Add this line
]

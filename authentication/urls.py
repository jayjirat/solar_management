from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'), 
    path('api/register/', views.register, name='register'),
    path('api/get_users/', views.get_users, name='get_users'),
    path('signup/', views.signup, name='signup'),
]

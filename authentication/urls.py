from django.urls import path
from . import views
from .views import ThammasatLoginAPI

urlpatterns = [
    path('', views.home, name='home'), 
    path("login/tu/", ThammasatLoginAPI.as_view(), name="tu-login"),
]
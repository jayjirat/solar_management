from django.shortcuts import render
from authentication.models import CustomUser
# Create your views here.


def users_management(request):
    users = CustomUser.objects.all()
    context = {'users': users}
    return render(request, 'users_management.html',context=context)


def dashboard(request):
    return render(request, 'dashboard.html')


def solar(request):
    return render(request, 'solar_management.html')


def upload(request):
    return render(request, 'upload_history.html')


def reports(request):
    return render(request, 'reports.html')

def profile(request):
    return render(request, 'profile.html')


def create_power_plant(request):
    return render(request, 'create_power_plant.html')

from django.shortcuts import render

# Create your views here.
def users_management(request):
    return render(request, 'users_management.html')

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
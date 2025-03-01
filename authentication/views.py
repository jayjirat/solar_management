from django.shortcuts import render

def home(request):
    return render(request, 'home.html') 



def users_management(request):
    return render(request, 'admin/users_management.html')

def dashboard(request):
    return render(request, 'admin/dashboard.html')

def solar(request):
    return render(request, 'admin/solar_management.html')

def upload(request):
    return render(request, 'admin/upload_history.html')

def reports(request):
    return render(request, 'admin/reports.html')
from django.shortcuts import redirect, render
from authentication.models import CustomUser
# Create your views here.


def users_management(request):
    users = CustomUser.objects.all()
    context = {'users': users}
    return render(request, 'users_management.html',context=context)

def users_management_manage(request,user_id):
    customuser = CustomUser.objects.get(id=user_id)

    if request.method == 'POST':
        customuser.role = request.POST.get('role')
        customuser.status = request.POST.get('status')
        customuser.save()
        return redirect('users_management')

    return render(request, 'users_management_manage.html', {
        'customuser': customuser,
        'roles': [('admin', 'Admin'), ('data_analyst', 'Data Analyst'),('drone_controller', 'Drone Controller')],
        'statuses': [('active', 'Active'), ('inactive', 'Inactive')],
    })

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

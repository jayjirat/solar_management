from django.shortcuts import render, redirect
from .forms import ImageUploadForm
from .models import PowerPlant, Zone

# Create your views here.


def users_management(request):
    return render(request, 'users_management.html')


def dashboard(request):
    return render(request, 'dashboard.html')


def solar(request):
    return render(request, 'solar_management.html')


def upload(request):
    # if request.method == 'POST':
    #     form = ImageUploadForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('upload_image')
    # else:
    #     form = ImageUploadForm()

    # powerplants = PowerPlant.objects.all()
    return render(request, 'upload_history.html') # , {'form': form, 'powerplants': powerplants})


def reports(request):
    return render(request, 'reports.html')

def profile(request):
    return render(request, 'profile.html')


def create_power_plant(request):
    return render(request, 'create_power_plant.html')

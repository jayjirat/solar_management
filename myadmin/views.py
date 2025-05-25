from django.shortcuts import render, redirect
from django.conf import settings
from .models import PowerPlant, CustomUser, Zone
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


def create_powerplant(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        # address isn't in model, just used for display
        address = request.POST.get('address')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        zone_name = request.POST.get('zone_name')
        height = request.POST.get('zone_height')
        width = request.POST.get('zone_width')

        if name and latitude and longitude:
            powerplant = PowerPlant.objects.create(
                name=name,
                latitude=float(latitude),
                longitude=float(longitude),
                total_tasks=0  # default or calculate if needed
            )
            # Create Zone if all fields provided
            if zone_name and height and width:
                Zone.objects.create(
                    name=zone_name,
                    powerplant=powerplant,
                    height=int(height),
                    width=int(width)
                )

            # Optionally, assign logged-in user or others to M2M roles here if needed
            # replace with your redirect target
            return redirect('solar_management')

    return render(request, 'create_powerplant.html', {
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY
    })

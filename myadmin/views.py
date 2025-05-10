from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from .forms import ImageUploadForm
from .models import PowerPlant, Zone, ImageUpload, SolarCell, CustomUser

# Users & Profile Management
def users_management(request):
    return render(request, 'users_management.html')

def profile(request):
    return render(request, 'profile.html')

def update_display_name(request):
    if request.method == "POST":
        display_name = request.POST.get("display_name")
        custom_user = CustomUser.objects.get(user=request.user)
        custom_user.display_name = display_name
        custom_user.save()
    return redirect('profile')

def upload_profile_image(request):
    if request.method == 'POST' and request.FILES.get('profile_image'):
        custom_user = CustomUser.objects.get(user=request.user)
        custom_user.profile_image = request.FILES['profile_image']
        custom_user.save()
    return redirect('profile')


# Dashboard & Management Pages
def dashboard(request):
    return render(request, 'dashboard.html')

def solar(request):
    return render(request, 'solar_management.html')

def reports(request):
    return render(request, 'reports.html')


# Upload Images
def upload(request):
    powerplants = PowerPlant.objects.all()
    zones = Zone.objects.all()

    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        powerplant_id = request.POST.get('powerplant')
        zone_id = request.POST.get('zone')

        if form.is_valid() and powerplant_id and zone_id:
            image_upload = form.save(commit=False)
            image_upload.powerplant = PowerPlant.objects.get(id=powerplant_id)
            image_upload.zone = Zone.objects.get(id=zone_id)
            image_upload.save()
            return redirect('upload_history')  # Replace with actual URL name

    else:
        form = ImageUploadForm()

    return render(request, 'upload_history.html', {
        'form': form,
        'powerplants': powerplants,
        'zones': zones
    })

def get_zones(request, powerplant_id):
    try:
        powerplant = PowerPlant.objects.get(id=powerplant_id)
        zones = powerplant.zone.all()
        zones_data = [{'id': zone.id, 'name': zone.name} for zone in zones]
        return JsonResponse({'zones': zones_data})
    except PowerPlant.DoesNotExist:
        return JsonResponse({'error': 'PowerPlant not found'}, status=404)


# PowerPlant Creation
def create_powerplant(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address')  # Not stored in DB
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        if name and latitude and longitude:
            PowerPlant.objects.create(
                name=name,
                latitude=float(latitude),
                longitude=float(longitude),
                total_tasks=0
            )
            return redirect('solar_management')

    return render(request, 'create_powerplant.html', {
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY
    })


# Report Detail
def report_detail(request):
    solar_data = [
        {
            'row': 2,
            'col': 2,
            'zone_name': 'Zone Keos',
            'zone_data': [
                [{'label': 'Metric A', 'value': 0.9}, {'label': 'Metric B', 'value': 0.6}],
                [{'label': 'Metric C', 'value': 0.2}, {'label': 'Metric D', 'value': 0.4}]
            ]
        },
        {
            'row': 4,
            'col': 1,
            'zone_name': 'Zone Theo',
            'zone_data': [
                [{'label': 'Metric E', 'value': 0.8}],
                [{'label': 'Metric F', 'value': 0.4}],
                [{'label': 'Metric G', 'value': 0.2}],
                [{'label': 'Metric H', 'value': 0.6}]
            ]
        },
    ]

    for zone in solar_data:
        for row in zone['zone_data']:
            for panel in row:
                panel['color_class'] = get_color(panel['value'])
        zone['row_range'] = range(zone['row'])
        zone['val_range'] = range(zone['col'])

    context = {
        'zone_amount': len(solar_data),
        'solar_data': solar_data
    }
    return render(request, 'report_detail.html', context)


# Helper
def get_color(value):
    if value >= 0.75:
        return 'bg-100-color'
    elif value >= 0.5:
        return 'bg-75-color'
    elif value >= 0.25:
        return 'bg-50-color'
    else:
        return 'bg-25-color'

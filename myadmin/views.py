from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from .forms import ImageUploadForm
from .models import PowerPlant, Zone, ImageUpload, SolarCell, CustomUser, ReportResult, Report, CellEfficiency
import csv
import io
from .forms import CSVUploadForm

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
def report_detail(request, report_id):
    report = Report.objects.get(id=report_id)
    report_result_list = ReportResult.objects.filter(report=report)
    solar_data = []
    for report_result in report_result_list:
        zone = report_result.zone
        x = zone.width
        y = zone.height
        zone_data = []
        sorted_solar_cell_list = SolarCell.objects.filter(zone=zone).order_by('y_position', 'x_position')
        eff_map = {
        e.solar_cell_id: e 
        for e in CellEfficiency.objects.filter(report_result=report_result)}
        cell_efficiencies = [eff_map.get(cell.id) for cell in sorted_solar_cell_list]
        print(cell_efficiencies)
        i = 0
        while i < len(cell_efficiencies):
            row_list = []
            for j in range(x):
                row_list.append({'value': cell_efficiencies[i].efficiency_percentage})
                i += 1
            zone_data.append(row_list)
        solar_data.append({'row': y, 'col': x, 'zone_name': zone.name, 'zone_data': zone_data})

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

def report_upload(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']

            if not csv_file.name.endswith('.csv'):
                return render(request, 'upload.html', {'form': form, 'error': 'File is not CSV'})

            decoded_file = csv_file.read().decode('utf-8')
            io_string = io.StringIO(decoded_file)
            reader = csv.DictReader(io_string)

            for row in reader:
                
                x_pos = int(row['x_pos'])
                y_pos = int(row['y_pos'])
                solar = SolarCell.objects.filter(zone_id='1',x_position=x_pos, y_position=y_pos)
                CellEfficiency.objects.create(
                    efficiency_percentage = row['efficiency'],
                    report_result_id = 1,
                    solar_cell_id = solar.id
                )

            return redirect('success_page')  # Change this as needed
    else:
        form = CSVUploadForm()
    return render(request, 'upload.html', {'form': form})


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

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Exists, OuterRef, Q
from .forms import ImageUploadForm, CSVUploadForm, ReportForm
from .models import PowerPlant, Zone, ImageUpload, SolarCell, ReportResult, Report, CellEfficiency
import csv
import io
from django.urls import reverse
from authentication.models import CustomUser
from .forms import ImageUploadForm
from .models import *
from django.core.serializers.json import DjangoJSONEncoder
import json
from myadmin.decorators import role_required

# Users & Profile Management
def users_management(request):
    users = CustomUser.objects.all()
    context = {'users': users}
    return render(request, 'users_management.html',context=context)

def users_management_manage(request,user_id):
    customuser = CustomUser.objects.get(id=user_id)
    
    back_url = request.META.get('HTTP_REFERER', reverse('users_management'))

    if request.method == 'POST':
        customuser.status = request.POST.get('status')
        customuser.save()
        return redirect('users_management')

    return render(request, 'users_management_manage.html', {
        'customuser': customuser,
        'statuses': [('active', 'Active'), ('inactive', 'Inactive')],
        'back_url': back_url
    })
def profile(request):
    custom_user = CustomUser.objects.get(user=request.user)
    context = {
        'custom_user': custom_user,
        'display_name': custom_user.display_name or request.user.username,
        'role': custom_user.role,
        'email': request.user.email,
        'profile_image': custom_user.profile_image,
    }
    return render(request, 'profile.html', context)


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
    powerplants = PowerPlant.objects.all()

    # Build a dictionary of all powerplant data
    powerplant_data = []

    for plant in powerplants:
        reports = Report.objects.filter(powerplant=plant).order_by('createdAt')
        report_data = [
            {
                "date": r.createdAt.strftime("%Y-%m-%d"),
                "energy": r.energy_generated
            }
            for r in reports
        ]

        powerplant_data.append({
            "id": plant.id,
            "name": plant.name,
            "zone": plant.zone.name if hasattr(plant, 'zone') else "",
            "panel": plant.panel.name if hasattr(plant, 'panel') else "",
            "reports": report_data
        })

    return render(request, 'dashboard.html', {
        "powerplants": powerplants,
        "powerplant_json": json.dumps(powerplant_data, cls=DjangoJSONEncoder)
    })

def solar(request):
    powerplants = PowerPlant.objects.all()

    context = {
        'powerplants': powerplants
    }
    return render(request, 'solar_management.html',context)

def solar_manage(request,powerplant_id):
    powerplant = PowerPlant.objects.get(id=powerplant_id)
    zones = Zone.objects.filter(powerplant=powerplant)
    solar_cells = SolarCell.objects.filter(zone__in=zones)
    reports = Report.objects.filter(powerplant=powerplant)
    users = CustomUser.objects.all()

    if request.method == "POST":
        user_id = request.POST.get("user_id")
        role = request.POST.get("role")
        user = CustomUser.objects.get(id=user_id)

        # ตรวจสอบว่า user มี role ไหนแล้วใน powerplant นี้หรือยัง
        already_has_role = (
            powerplant.admin.filter(id=user.id).exists() or
            powerplant.data_analyst.filter(id=user.id).exists() or
            powerplant.drone_controller.filter(id=user.id).exists()
        )

        if already_has_role:
            return redirect('solar_management_manage', powerplant_id=powerplant_id)
        else:
            if role == 'admin':
                powerplant.admin.add(user)
                user.role = 'admin'
            elif role == 'data_analyst':
                powerplant.data_analyst.add(user)
                user.role = 'data_analyst'
            elif role == 'drone_controller':
                powerplant.drone_controller.add(user)
                user.role = 'drone_controller'
            powerplant.save()
            user.save()
            return redirect('solar_management_manage', powerplant_id=powerplant_id)



    context = {
        'powerplant': powerplant,
        'zones' : zones,
        'solar_cells': solar_cells,
        'reports': reports,
        'roles': [('admin', 'Admin'), ('data_analyst', 'Data Analyst'),('drone_controller', 'Drone Controller')],
        'users': users
    }
    return render(request, 'solar_management_manage.html',context)


def upload(request):
    return render(request, 'upload_history.html')


def reports(request):
    query = request.GET.get('q', '')
    user = request.user
    custom_user = getattr(user, 'custom', None)

    # Base queryset with annotation
    reports = Report.objects.select_related('powerplant', 'reporter__user').annotate(
        has_result=Exists(
            ReportResult.objects.filter(report=OuterRef('pk'))
        )
    )

    # Only filter if not superadmin
    if custom_user and custom_user.role != 'superadmin':
        reports = reports.filter(
            Q(powerplant__admin=custom_user) |
            Q(powerplant__data_analyst=custom_user) |
            Q(powerplant__drone_controller=custom_user)
        ).distinct()

    # Apply search filter
    if query:
        reports = reports.filter(
            Q(powerplant__name__icontains=query) |
            Q(id__icontains=query)
        )

    # Paginate results
    paginator = Paginator(reports, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'reports.html', {'page_obj': page_obj, 'query': query})


# Upload Images
@role_required('admin', 'superadmin', 'data_analyst')
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

# Report Detail
@role_required('admin', 'superadmin', 'data_analyst')
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

    powerplant = report.powerplant
    context = {
        'zone_amount': len(solar_data),
        'solar_data': solar_data,
        'report': report,
        'powerplant': powerplant,
    }
    return render(request, 'report_detail.html', context)

@role_required('admin', 'superadmin', 'data_analyst')
def create_report(request):
    try:
        custom_user = CustomUser.objects.get(user=request.user)
        if request.method == 'POST':
            form = ReportForm(request.POST, user=request.user)
            if form.is_valid():
                report = form.save(commit=False)
                report.reporter = custom_user
                report.save()
                return redirect('reports')  
        else:
            form = ReportForm(user=request.user)
        return render(request, 'create_report.html', {'form': form})
    except CustomUser.DoesNotExist:
        return render(request, 'errors/missing_profile.html', status=404)

@role_required('admin', 'superadmin', 'data_analyst')
def report_upload(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    powerplant = report.powerplant
    zones = Zone.objects.filter(powerplant=powerplant)
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():

            csv_file = form.cleaned_data['csv_file']

            if not csv_file.name.endswith('.csv'):
                return render(request, 'upload_report.html', {'form': form, 'error': 'File is not CSV'})
            
            decoded_file = csv_file.read().decode('utf-8')
            io_string = io.StringIO(decoded_file)
            reader = csv.DictReader(io_string)
            for zone in zones:
                ReportResult.objects.create(
                    report = report,
                    zone = zone,
                )
            for row in reader:
                zone_name = row['zone_name']
                x_pos = int(row['x_pos'])
                y_pos = int(row['y_pos'])
                try:
                    zone_id = Zone.objects.get(powerplant=powerplant, name=zone_name)
                    report_result = ReportResult.objects.get(report=report, zone_id=zone_id)
                    solar = SolarCell.objects.get(zone_id=zone_id, x_position=x_pos, y_position=y_pos)
                except Zone.DoesNotExist:
                    continue
                except SolarCell.DoesNotExist:
                    continue # write handle
                except:
                    continue

                CellEfficiency.objects.create(
                    efficiency_percentage = float(row['efficiency']),
                    report_result = report_result,
                    solar_cell_id = solar.id
                )

            return redirect('reports')  # Change this as needed
    else:
        form = CSVUploadForm()

    context = {
        'form': form,
        'zones': zones,
        'report': report,
        'powerplant': powerplant,
    }
    return render(request, 'upload_report.html', context)

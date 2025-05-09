from .models import PowerPlant, CustomUser
from django.conf import settings
from django.shortcuts import render, redirect, redirect
from .forms import ImageUploadForm
from .models import PowerPlant, Zone, ImageUpload, SolarCell
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse

# Create your views here.


def users_management(request):
    return render(request, 'users_management.html')


def dashboard(request):
    return render(request, 'dashboard.html')


def solar(request):
    return render(request, 'solar_management.html')


from .models import PowerPlant, Zone, SolarCell
from django.shortcuts import render, redirect, get_object_or_404

from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import PowerPlant, Zone
from .forms import ImageUploadForm

def upload(request):
    powerplants = PowerPlant.objects.all()

    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        powerplant_id = request.POST.get('powerplant')
        zone_id = request.POST.get('zone')

        print(f"Selected PowerPlant ID: {powerplant_id}")
        print(f"Selected Zone ID: {zone_id}")

        # ตรวจสอบว่า PowerPlant มีอยู่ในฐานข้อมูลหรือไม่ ถ้าไม่มีก็สร้างใหม่
        try:
            powerplant = PowerPlant.objects.get(id=powerplant_id)
        except PowerPlant.DoesNotExist:
            print(f"PowerPlant with ID {powerplant_id} does not exist. Creating a new one.")
            # สร้าง PowerPlant ใหม่ ถ้าไม่พบ
            powerplant = PowerPlant.objects.create(id=powerplant_id, name=f"PowerPlant {powerplant_id}",
                                                   latitude=0.0, longitude=0.0, total_tasks=0)
        
        # ตรวจสอบว่า Zone มีอยู่ในฐานข้อมูลหรือไม่ ถ้าไม่มีก็สร้างใหม่
        try:
            zone = Zone.objects.get(id=zone_id)
        except Zone.DoesNotExist:
            print(f"Zone with ID {zone_id} does not exist. Creating a new one.")
            zone = Zone.objects.create(id=zone_id, name=f"Zone {zone_id}", powerplant=powerplant)

        # ตรวจสอบว่า Form valid หรือไม่
        if form.is_valid():
            solar_cell = form.save(commit=False)
            solar_cell.zone = zone  # กำหนดโซนจากฟอร์ม
            solar_cell.save()
            return redirect('upload_history')
        else:
            print("Form invalid or missing zone/powerplant")

    else:
        form = ImageUploadForm()

    return render(request, 'upload_history.html', {
        'form': form,
        'powerplants': powerplants
    })

def get_zones(request, powerplant_id):
    try:
        powerplant = PowerPlant.objects.get(id=powerplant_id)
        zones = powerplant.zone.all()
        zones_data = [{'id': zone.id, 'name': zone.name} for zone in zones]
        return JsonResponse({'zones': zones_data})
    except PowerPlant.DoesNotExist:
        return JsonResponse({'error': 'PowerPlant not found'}, status=404)



def reports(request):
    return render(request, 'reports.html')


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


def create_powerplant(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        # address isn't in model, just used for display
        address = request.POST.get('address')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        if name and latitude and longitude:
            powerplant = PowerPlant.objects.create(
                name=name,
                latitude=float(latitude),
                longitude=float(longitude),
                total_tasks=0  # default or calculate if needed
            )
            # Optionally, assign logged-in user or others to M2M roles here if needed
            # replace with your redirect target
            return redirect('solar_management')

    return render(request, 'create_powerplant.html', {
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY
    })

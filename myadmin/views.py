from .models import PowerPlant, CustomUser
from django.conf import settings
from django.shortcuts import render, redirect, redirect
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
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('upload_image')
    else:
        form = ImageUploadForm()

    powerplants = PowerPlant.objects.all()
    return render(request, 'upload_history.html', {'form': form, 'powerplants': powerplants})

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

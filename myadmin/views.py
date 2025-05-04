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


def create_power_plant(request):
    return render(request, 'create_power_plant.html')

def report_detail(request):
    data_list = [
    {'label': 'Metric A', 'value': 0.9},
    {'label': 'Metric B', 'value': 0.6},
    {'label': 'Metric C', 'value': 0.2},]

    for item in data_list:
        item['color_class'] = get_color(item['value'])
    
    # will add more basic info later
    context = {
        'zone_amount': 2,
        'data_list': data_list}
    return render(request, 'report_detail.html', context)


# helper function for report_detail
def get_color(value):
    if value >= 0.75:
        return 'text-success'
    elif value >= 0.4:
        return 'text-warning'
    else:
        return 'text-error'
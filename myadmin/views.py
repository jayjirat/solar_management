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
    solar_data = [{
        'row': 2,
        'col': 2,
        'zone_name': 'Zone Keos',
        'zone_data': [
            [ {'label': 'Metric A', 'value': 0.9},
            {'label': 'Metric B', 'value': 0.6},],
            [{'label': 'Metric C', 'value': 0.2},
            {'label': 'Metric D', 'value': 0.4},]
            ]
    },
    {
        'row': 4,
        'col': 1,
        'zone_name': 'Zone Theo',
        'zone_data': [
            [ {'label': 'Metric E', 'value': 0.8}],
            [{'label': 'Metric F', 'value': 0.4}],
            [{'label': 'Metric G', 'value': 0.2}],
            [{'label': 'Metric H', 'value': 0.6}]
            ]
    },
    ]
    
    for zone in solar_data:
        zone_data = zone['zone_data']
        for row in zone_data:
            for panel in row: 
                panel['color_class'] = get_color(panel['value'])
    
    for zone in solar_data:
        row_val = zone['row']
        zone['row_range'] = range(row_val)
    
    for zone in solar_data:
        col_val = zone['col']
        zone['val_range'] = range(col_val)

    # will add more basic info later
    context = {
        'zone_amount': 2,
        'solar_data': solar_data}
    return render(request, 'report_detail.html', context)


# helper function for report_detail
def get_color(value):
    if value >= 0.75:
        return 'bg-100-color'
    elif value >= 0.5:
        return 'bg-75-color'
    elif value >= 0.25:
        return 'bg-50-color'
    else:
        return 'bg-25-color'
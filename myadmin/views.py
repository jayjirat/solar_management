from django.shortcuts import render

from authentication.models import CustomUser

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
    context = {}  # Initialize an empty context dictionary
    
    if request.user.is_authenticated:
        user = request.user  # Get the current logged-in user
        print(f"Current user: {user}")  # Debugging print for user
        
        # Add basic user data to context
        context['username'] = user.username.split('@')[0]
        context['email'] = user.email
        context['first_name'] = user.first_name
        context['last_name'] = user.last_name
        
        try:
            # Fetch the related CustomUser instance
            custom_user = CustomUser.objects.get(user=user)
            print(f"CustomUser data: {custom_user}")  # Debugging print for CustomUser
            
            # Add CustomUser data to context
            context['role'] = custom_user.role
            
        except CustomUser.DoesNotExist:
            context['role'] = "user"  # Default role if CustomUser is not found
            print(f"CustomUser not found for user: {user.username}")
    else:
        context['not_authenticated'] = True
    
    # Pass the context to the template
    return render(request, 'profile.html', context)


def create_power_plant(request):
    return render(request, 'create_power_plant.html')

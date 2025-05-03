from .models import CustomUser

def global_user_context(request):
    if request.user.is_authenticated:
        try:
            custom_user = CustomUser.objects.get(user=request.user)
            return {
                'username': request.user.username,
                'email': request.user.email,
                'role': custom_user.role,
                'display_name': custom_user.display_name or request.user.username.split('@')[0]
            }
        except CustomUser.DoesNotExist:
            return {}
    return {}

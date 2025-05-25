from functools import wraps
from django.core.exceptions import PermissionDenied

def role_required(*roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                raise PermissionDenied
            if not hasattr(request.user, 'custom'):
                raise PermissionDenied
            if request.user.custom.role not in roles:
                raise PermissionDenied
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

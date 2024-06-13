from functools import wraps
from rest_framework.exceptions import PermissionDenied

def restrict_to_owner(view_func):
    @wraps(view_func)
    def _wrapped_view(view_instance, request, *args, **kwargs):
        # Check if the user is the owner of the requested resource
        if hasattr(view_instance, 'get_object'):
            obj = view_instance.get_object()
        else:
            obj = None

        if obj and hasattr(obj, 'user') and obj.user != request.user:
            raise PermissionDenied("You don't have permission to access this resource.")

        return view_func(view_instance, request, *args, **kwargs)

    return _wrapped_view

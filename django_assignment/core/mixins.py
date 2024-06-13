# mixins.py
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from .models import PlatformApiCall

class PlatformApiCallMixin:
    def finalize_response(self, request, response, *args, **kwargs):
        if request.user.is_authenticated:
            PlatformApiCall.objects.create(
                user=request.user,
                requested_url=request.build_absolute_uri(),
                requested_data=request.data,
                response_data=response.data if isinstance(response, Response) else {}
            )
        return super().finalize_response(request, response, *args, **kwargs)

from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.models import User

class TokenAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = request.GET.get('token')
        if token and token == getattr(settings, 'ASSET_CHECK_TOKEN', None):
            if not request.user.is_authenticated:
                try:
                    user = User.objects.get(username='menti')
                    user.backend = 'django.contrib.auth.backends.ModelBackend'
                    login(request, user)
                except User.DoesNotExist:
                    pass
        return self.get_response(request)

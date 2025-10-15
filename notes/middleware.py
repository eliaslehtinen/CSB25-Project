from django.core.cache import cache
from django.conf import settings
from django.http import HttpResponseForbidden

# Based on https://unfoldai.com/preventing-brute-force-with-django-middleware/
class BruteForceProtectionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # If login attempt
        if (request.path == "/admin/login/" or request.path == "/login/") and request.method == "POST":
            # Source ip of login attempt
            ip_address = request.META.get("REMOTE_ADDR")

            # Amount of failed login attempts is stored in cache
            cache_key = f"login_attempts:{ip_address}"
            login_attempts = cache.get(cache_key, 0)
            # If failed login attempt, increment number in cache
            if not request.user.is_authenticated:
                cache.set(cache_key, login_attempts + 1, timeout=settings.BRUTE_FORCE_TIMEOUT)
            
            # If more failed login attempts than allowed, block attempts until timeout ends
            if login_attempts >= settings.BRUTE_FORCE_TRESHOLD:
                return HttpResponseForbidden(
                    f"Too many login attempts. Please wait {settings.BRUTE_FORCE_TIMEOUT // 60} minutes and try again."
                )
        return response
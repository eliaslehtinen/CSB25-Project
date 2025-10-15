from django.core.cache import cache
from django.conf import settings
from django.http import HttpResponseForbidden

# Based on https://unfoldai.com/preventing-brute-force-with-django-middleware/
class BruteForceProtectionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        print(response)

        # If login attempt
        if "login" in request.path and request.method == "POST":
            # Source ip of login attempt
            ip_address = request.META.get("REMOTE_ADDR")
            print(ip_address)

            # Amount of failed login attempts is stored in cache
            cache_key = f"failed_login_attempts:{ip_address}"
            login_attempts = cache.get(cache_key, 0)
            # If failed login attempt, increment number in cache
            if response.status_code != 200:
                cache.set(cache_key, login_attempts + 1, timeout=settings.BRUTE_FORCE_TIMEOUT)
            else:
                cache.set(cache_key, 0)
            
            # If more failed login attempts than allowed, block attempts until timeout ends
            if login_attempts >= settings.BRUTE_FORCE_TRESHOLD:
                return HttpResponseForbidden(
                    f"Too many login attempts. Please wait {settings.BRUTE_FORCE_TIMEOUT // 60} minutes and try again."
                )
        return response
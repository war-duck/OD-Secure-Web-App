from django.http import HttpResponseForbidden
from .models import BlockedIP

class IPBlockMiddleware:
    def __init__(self, get_response):
            self.get_response = get_response

    def __call__(self, request):
        ip_address = self.get_client_ip(request)
        if BlockedIP.objects.filter(ip=ip_address).exists():
            return HttpResponseForbidden("Your IP address has been blocked.")
        response = self.get_response(request)
        return response
        
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
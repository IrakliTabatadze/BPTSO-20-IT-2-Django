from django.http import HttpResponseForbidden
from django.conf import settings

class IpBlockMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        ip = request.META.get('REMOTE_ADDR')

        if ip in settings.BLOCKED_IPS:
            return HttpResponseForbidden('<h1>You Are Blocked</h1>')


        response = self.get_response(request)

        return response
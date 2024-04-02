from django.conf import settings
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin

class CustomXFrameOptionsMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        response['X-Frame-Options'] = 'ALLOWALL'
        return response
class PreventLoginAfterAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        if request.user.is_authenticated and request.path == settings.LOGIN_URL:
            return redirect(settings.LOGIN_REDIRECT_URL)
        
        return response

from django.shortcuts import redirect
from django.urls import reverse
from django.http import JsonResponse
import logging

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        exempt_urls = [reverse('store:login'), reverse('store:register'), '/admin/']

        if not request.user.is_authenticated:
            path = request.path_info
            if not any(path.startswith(url) for url in exempt_urls):
                return redirect('store:login')

        response = self.get_response(request)
        return response
    
class ErrorHandlingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
            return response
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
        

logger = logging.getLogger(__name__)

class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger.info(f"Request by user: {request.user}")
        logger.info(f"Request: {request.method} {request.path}")
        response = self.get_response(request)
        logger.info(f"Response Status: {response.status_code}")
        return response
from django.shortcuts import redirect
from django.urls import reverse
from django.http import JsonResponse
import logging
from pymongo import MongoClient
import datetime

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
        
client = MongoClient("mongodb://localhost:27017/")
db = client["ecommer_logs"]
logs_collection = db["logs"]

logger = logging.getLogger(__name__)

def mongo_log(user,action,details=None):
    log = {
        "user_id": getattr(user, "id", None),
        "username": getattr(user, "username", "Anonymous"),
        "action": action,
        "details": details or {},
        "timestamp": datetime.datetime.now(datetime.timezone.utc)
    }
    logs_collection.insert_one(log)

class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, "user", None)
        mongo_log(user, "request", {"method":request.method,"path":request.path})
        logger.info(f"Request by user: {request.user}")
        logger.info(f"Request: {request.method} {request.path}")
        response = self.get_response(request)
        mongo_log(user,"response",{"status_code":response.status_code})
        logger.info(f"Response Status: {response.status_code}")
        return response

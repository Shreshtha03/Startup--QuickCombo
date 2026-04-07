from django.http import HttpResponse

class ForceCorsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'OPTIONS':
            response = HttpResponse()
            response.status_code = 200
        else:
            response = self.get_response(request)
        
        # Force allow ALL
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, PATCH, DELETE, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'X-Admin-Password, x-admin-password, x-user-email, Content-Type, Authorization, X-CSRFToken, X-Requested-With'
        response['Access-Control-Allow-Credentials'] = 'true'
        response['Access-Control-Max-Age'] = '86400' # 24 hours
        return response

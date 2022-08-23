from django.core.handlers.wsgi import WSGIRequest


class PermissionsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: WSGIRequest):
        response = self.get_response(request)
        return response

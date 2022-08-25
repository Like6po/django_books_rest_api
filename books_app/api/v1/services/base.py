from rest_framework.request import Request

from api.v1.services.misc import decorate_class_methods, pass_exception_http_500


@decorate_class_methods(pass_exception_http_500)
class BaseService:
    def __init__(self, request: Request):
        self.request = request

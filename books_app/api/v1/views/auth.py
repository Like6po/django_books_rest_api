from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api.v1.models.user import User
from api.v1.services.auth import AuthService


class RegisterUserView(APIView):
    def post(self, request: Request):
        auth = AuthService(request)
        result = auth.register(role=User.ROLES.USER.value)
        return Response(result, status=result["status_code"])


class RegisterAuthorView(APIView):
    def post(self, request: Request):
        auth = AuthService(request)
        result = auth.register(role=User.ROLES.AUTHOR.value)
        return Response(result, status=result["status_code"])


class LoginView(APIView):
    def post(self, request: Request):
        auth = AuthService(request)
        result = auth.login()
        return Response(result, status=result["status_code"])


class RefreshView(APIView):
    def post(self, request: Request):
        auth = AuthService(request)
        result = auth.refresh()
        return Response(result, status=result["status_code"])

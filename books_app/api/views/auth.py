from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models.author import Author
from api.serializers.auth import RegisterAuthorSerializer, LoginAuthorSerializer, RefreshAuthorSerializer
from api.token import AccessJWToken, RefreshJWToken


class RegisterView(APIView):
    serializer_class = RegisterAuthorSerializer

    def post(self, request: Request):
        serializer = RegisterAuthorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        author: Author = serializer.create(serializer.validated_data)
        return Response({"id": author.id,
                         "full_name": author.full_name(),
                         }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    serializer_class = LoginAuthorSerializer

    def post(self, request: Request):
        serializer = LoginAuthorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        _, access_token = AccessJWToken()(user_identifier=serializer.validated_data["author_id"])
        _, refresh_token = RefreshJWToken()()

        return Response({"access_token": access_token,
                         "refresh_token": refresh_token}, status=200)


class RefreshView(APIView):
    serializer_class = RefreshAuthorSerializer

    def post(self, request: Request):
        serializer = RefreshAuthorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        _, access_token = AccessJWToken()(str(serializer.token.sub))
        _, refresh_token = RefreshJWToken()()

        return Response({"access_token": access_token,
                         "refresh_token": refresh_token}, status=200)

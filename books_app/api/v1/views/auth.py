from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api.v1.models.author import Author
from api.v1.models.token import Token
from api.v1.serializers.auth import RegisterAuthorSerializer, LoginAuthorSerializer, RefreshAuthorSerializer
from api.v1.token import AccessJWToken, RefreshJWToken


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

        refresh_token_db = Token.objects.filter(author_id=serializer.validated_data["author_id"], is_active=True)
        if not refresh_token_db:
            _, refresh_token = RefreshJWToken()()
            Token.objects.create(author_id=serializer.validated_data["author_id"],
                                 token=refresh_token)

        refresh_token = refresh_token_db.first().token
        try:
            _ = RefreshJWToken(refresh_token)
        except ValueError:
            try:
                Token.objects.get(token=refresh_token).delete()
            except Token.DoesNotExist:
                pass
            _, refresh_token = RefreshJWToken()()
            Token.objects.create(author_id=serializer.validated_data["author_id"],
                                 token=refresh_token)

        return Response({"access_token": access_token,
                         "refresh_token": refresh_token}, status=200)


class RefreshView(APIView):
    serializer_class = RefreshAuthorSerializer

    def post(self, request: Request):
        serializer = RefreshAuthorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        refresh_token = serializer.validated_data["refresh_token"]
        try:
            refresh_token_db = Token.objects.get(token=refresh_token)
            refresh_token_db.delete()
            if not refresh_token_db.is_active:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        except Token.DoesNotExist:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        subject = refresh_token_db.author.id
        _, access_token = AccessJWToken()(str(subject))
        _, refresh_token = RefreshJWToken()()
        Token.objects.create(author_id=str(subject),
                             token=refresh_token)

        return Response({"access_token": access_token,
                         "refresh_token": refresh_token}, status=status.HTTP_200_OK)

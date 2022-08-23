from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api.v1.models.token import Token
from api.v1.models.user import User
from api.v1.serializers.auth import RegisterUserSerializer, LoginUserSerializer, RefreshUserSerializer
from api.v1.token import AccessJWToken, RefreshJWToken


class RegisterUserView(APIView):
    def post(self, request: Request):
        serializer = RegisterUserSerializer(data=request.data,
                                            context={"role": User.ROLES.USER.value})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        _, access_token = AccessJWToken()(user_identifier=str(serializer.data["id"]))
        _, refresh_token = RefreshJWToken()()
        Token.objects.create(author_id=serializer.data["id"],
                             token=refresh_token)
        return Response({"id": serializer.data["id"],
                         "email": serializer.data["email"],
                         "first_name": serializer.data["first_name"],
                         "second_name": serializer.data["second_name"],
                         "access_token": access_token,
                         "refresh_token": refresh_token}, status=status.HTTP_201_CREATED)


class RegisterAuthorView(APIView):
    def post(self, request: Request):
        serializer = RegisterUserSerializer(data=request.data,
                                            context={"role": User.ROLES.AUTHOR.value})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        _, access_token = AccessJWToken()(user_identifier=str(serializer.data["id"]))
        _, refresh_token = RefreshJWToken()()
        Token.objects.create(author_id=serializer.data["id"],
                             token=refresh_token)
        return Response({"id": serializer.data["id"],
                         "email": serializer.data["email"],
                         "first_name": serializer.data["first_name"],
                         "second_name": serializer.data["second_name"],
                         "access_token": access_token,
                         "refresh_token": refresh_token}, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    def post(self, request: Request):
        serializer = LoginUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.get(email=serializer.validated_data["email"])

        _, access_token = AccessJWToken()(user_identifier=str(user.id))

        refresh_token_db = Token.objects.filter(author_id=user.id, is_active=True)
        if not refresh_token_db:
            _, refresh_token = RefreshJWToken()()
            Token.objects.create(author_id=user.id,
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
            Token.objects.create(author_id=user.id,
                                 token=refresh_token)

        return Response({"access_token": access_token,
                         "refresh_token": refresh_token}, status=status.HTTP_200_OK)


class RefreshView(APIView):
    serializer_class = RefreshUserSerializer

    def post(self, request: Request):
        serializer = RefreshUserSerializer(data=request.data)
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

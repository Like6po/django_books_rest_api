from typing import Union

from rest_framework import status

from api.tasks import send
from api.v1.consts import StatusValues
from api.v1.models.token import Token
from api.v1.models.user import User
from api.v1.serializers.auth import RegisterUserSerializer, LoginUserSerializer, RefreshUserSerializer
from api.v1.services.base import BaseService
from api.v1.services.misc import generate_code_from_email_and_password
from api.v1.token import AccessJWToken, RefreshJWToken


class AuthService(BaseService):
    @staticmethod
    def _create_access_token(subject: Union[int, float]) -> str:
        _, access_token = AccessJWToken()(user_identifier=str(subject))
        return access_token

    @staticmethod
    def _create_refresh_token(subject: Union[int, float]) -> str:
        _, refresh_token = RefreshJWToken()()
        Token.objects.create(author_id=str(subject),
                             token=refresh_token)
        return refresh_token

    def _get_or_create_refresh_token(self, subject: Union[int, str]) -> str:
        refresh_token_db = Token.objects.filter(author_id=str(subject), is_active=True)
        if not refresh_token_db:
            return self._create_refresh_token(subject)

        refresh_token = refresh_token_db.first().token

        try:
            _ = RefreshJWToken(refresh_token)
        except ValueError:
            try:
                Token.objects.get(token=refresh_token).delete()
            except Token.DoesNotExist:
                pass
            return self._create_refresh_token(subject)

        return refresh_token

    def register(self, role: User.ROLES) -> dict:
        serializer = RegisterUserSerializer(data=self.request.data,
                                            context={"role": role})
        if not serializer.is_valid():
            return {"detail": serializer.errors,
                    "status": StatusValues.FAILED.value,
                    "status_code": status.HTTP_400_BAD_REQUEST}

        code = generate_code_from_email_and_password(serializer.validated_data["email"], self.request.data["password"])

        if not (received_code := self.request.data.get("code", None)):
            send.delay("Код подтверждения",
                       f"Ваш код подтверждения: {code}",
                       serializer.validated_data["email"])
            return {"detail": "Waiting code",
                    "status": StatusValues.SUCCESS.value,
                    "status_code": status.HTTP_200_OK}

        if received_code != code:
            return {"detail": "Wrong code",
                    "status": StatusValues.SUCCESS.value,
                    "status_code": status.HTTP_403_FORBIDDEN}

        serializer.save()

        access_token = self._create_access_token(serializer.data["id"])
        refresh_token = self._create_refresh_token(serializer.data["id"])
        send.delay("Успешная регистрация",
                   f"Вы успешно зарегистрировались!",
                   serializer.validated_data["email"])
        return {"detail": {"id": serializer.data["id"],
                           "email": serializer.data["email"],
                           "first_name": serializer.data["first_name"],
                           "second_name": serializer.data["second_name"],
                           "access_token": access_token,
                           "refresh_token": refresh_token},
                "status": StatusValues.SUCCESS.value,
                "status_code": status.HTTP_201_CREATED}

    def login(self) -> dict:
        serializer = LoginUserSerializer(data=self.request.data)
        if not serializer.is_valid():
            return {"detail": serializer.errors,
                    "status": StatusValues.FAILED.value,
                    "status_code": status.HTTP_400_BAD_REQUEST}
        try:
            user = User.objects.get(email=serializer.validated_data["email"])
        except User.DoesNotExist:
            return {"detail": "User not found",
                    "status": StatusValues.FAILED.value,
                    "status_code": status.HTTP_404_NOT_FOUND}

        access_token = self._create_access_token(user.id)
        refresh_token = self._get_or_create_refresh_token(user.id)

        return {"detail": {"access_token": access_token,
                           "refresh_token": refresh_token},
                "status": StatusValues.SUCCESS.value,
                "status_code": status.HTTP_200_OK}

    def refresh(self) -> dict:
        serializer = RefreshUserSerializer(data=self.request.data)
        if not serializer.is_valid():
            return {"detail": serializer.errors,
                    "status": StatusValues.FAILED.value,
                    "status_code": status.HTTP_400_BAD_REQUEST}
        refresh_token = serializer.validated_data["refresh_token"]
        try:
            refresh_token_db = Token.objects.get(token=refresh_token)
            refresh_token_db.delete()
            if not refresh_token_db.is_active:
                return {"detail": "Token is deactivated",
                        "status": StatusValues.FAILED.value,
                        "status_code": status.HTTP_404_NOT_FOUND}
        except Token.DoesNotExist:
            return {"detail": "Token don't exists",
                    "status": StatusValues.FAILED.value,
                    "status_code": status.HTTP_404_NOT_FOUND}

        access_token = self._create_access_token(refresh_token_db.author.id)
        refresh_token = self._create_refresh_token(refresh_token_db.author.id)

        return {"detail": {"access_token": access_token,
                           "refresh_token": refresh_token},
                "status": StatusValues.SUCCESS.value,
                "status_code": status.HTTP_200_OK}

import datetime
from typing import Union

import bcrypt
from rest_framework import status

from api.tasks import send
from api.v1.consts import StatusValues
from api.v1.models.confirm_code import ConfirmCode
from api.v1.models.recovery_code import RecoveryCode
from api.v1.models.token import Token
from api.v1.models.user import User
from api.v1.serializers.auth import RegisterUserSerializer, LoginUserSerializer, RefreshUserSerializer, \
    RecoveryUserSerializer, ChangePasswordUserSerivalizer
from api.v1.services.base import BaseService
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

        serializer.save()

        access_token = self._create_access_token(serializer.data["id"])
        refresh_token = self._create_refresh_token(serializer.data["id"])

        confirm_code = ConfirmCode.objects.create(user_id=serializer.data["id"])

        send.delay("Подтверждение регистрации",
                   f"Для подтвреждения регистрации перейдите по ссылке:\n"
                   f"http://{self.request.META['HTTP_HOST']}/api/v1/confirm/{confirm_code.id}",
                   serializer.validated_data["email"])

        return {"detail": {"id": serializer.data["id"],
                           "email": serializer.data["email"],
                           "first_name": serializer.data["first_name"],
                           "second_name": serializer.data["second_name"],
                           "access_token": access_token,
                           "refresh_token": refresh_token},
                "status": StatusValues.SUCCESS.value,
                "status_code": status.HTTP_201_CREATED}

    def confirm(self) -> dict:
        code = self.request.parser_context.get("kwargs").get("code")
        try:
            code = ConfirmCode.objects.get(id=code)
        except ConfirmCode.DoesNotExist:
            return {"detail": "Link not valid",
                    "status": StatusValues.FAILED.value,
                    "status_code": status.HTTP_400_BAD_REQUEST}

        if not (datetime.datetime.utcnow().replace(tzinfo=None) - code.created_at.replace(tzinfo=None) <
                datetime.timedelta(minutes=5) and code.is_active):
            return {"detail": "Link not valid",
                    "status": StatusValues.FAILED.value,
                    "status_code": status.HTTP_400_BAD_REQUEST}

        code.user.is_active = True
        code.user.save()
        code.delete()
        send.delay("Подтверждение регистрации",
                   "Аккаунт успешно активирован!",
                   code.user.email)

        return {"detail": "Account activated",
                "status": StatusValues.SUCCESS.value,
                "status_code": status.HTTP_200_OK}

    def recovery(self) -> dict:
        serializer = RecoveryUserSerializer(data=self.request.data)
        if not serializer.is_valid():
            return {"detail": serializer.errors,
                    "status": StatusValues.FAILED.value,
                    "status_code": status.HTTP_400_BAD_REQUEST}

        recovery_code = RecoveryCode.objects.create(user=serializer.user)

        send.delay("Восстановление аккаунта",
                   "Ваш код восстановления:\n"
                   f"{recovery_code.id}",
                   serializer.validated_data["email"])

        return {"detail": "Waiting password",
                "status": StatusValues.SUCCESS.value,
                "status_code": status.HTTP_200_OK}

    def recovery_change_password(self) -> dict:
        serializer = ChangePasswordUserSerivalizer(data=self.request.data)
        if not serializer.is_valid():
            return {"detail": serializer.errors,
                    "status": StatusValues.FAILED.value,
                    "status_code": status.HTTP_400_BAD_REQUEST}
        code = self.request.parser_context.get("kwargs").get("code")
        try:
            recovery_code = RecoveryCode.objects.get(id=code)
        except RecoveryCode.DoesNotExist:
            return {"detail": "Link not valid",
                    "status": StatusValues.FAILED.value,
                    "status_code": status.HTTP_400_BAD_REQUEST}
        if not (datetime.datetime.utcnow().replace(tzinfo=None) - recovery_code.created_at.replace(tzinfo=None) <
                datetime.timedelta(minutes=5) and recovery_code.is_active):
            return {"detail": "Link not valid",
                    "status": StatusValues.FAILED.value,
                    "status_code": status.HTTP_400_BAD_REQUEST}

        recovery_code.user.password_hash = bcrypt.hashpw(serializer.validated_data["password"].encode('utf-8'),
                                                         bcrypt.gensalt()).decode("utf-8")
        recovery_code.user.save()
        recovery_code.delete()

        send.delay("Восстановление аккаунта",
                   "Ваш пароль успешно изменен",
                   recovery_code.user.email)

        return {"detail": "Password changed",
                "status": StatusValues.SUCCESS.value,
                "status_code": status.HTTP_200_OK}

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

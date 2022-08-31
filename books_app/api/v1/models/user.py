from typing import Union, Optional

from django.db import models

from api.v1.models.token import Token
from api.v1.token import AccessJWToken, RefreshJWToken


class User(models.Model):
    class Meta:
        db_table = "users"
        ordering = ["id"]
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    class ROLES(models.IntegerChoices):
        USER = 0, "Пользователь"
        AUTHOR = 1, "Автор"
        ADMIN = 2, "Администратор"

    id = models.AutoField("ID", primary_key=True)
    created_at = models.DateTimeField("Время регистрации", auto_now_add=True)
    first_name = models.CharField("Имя", max_length=128)
    second_name = models.CharField("Фамилия", max_length=128)
    patronymic = models.CharField("Отчество", max_length=128, blank=True, null=True, default=None)
    email = models.EmailField("Почта", null=True, default=None)
    password_hash = models.CharField("Хеш пароля", max_length=256)
    role = models.IntegerField("Роль", choices=ROLES.choices, default=ROLES.USER.value)
    is_active = models.BooleanField("Активен", default=False)

    def full_name(self):
        return f"{self.first_name} {self.second_name}"

    @property
    def fio(self):
        return f"{self.full_name()}" + (f" {self.patronymic}" if self.patronymic else "")

    full_name.short_description = "Полное имя"

    def __str__(self):
        return f"{self.fio} - {self.email}"

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    @property
    def is_admin(self):
        return self.role == self.ROLES.ADMIN.value

    @property
    def is_author(self):
        return self.role == self.ROLES.AUTHOR.value

    @staticmethod
    def _create_access_token(subject: Union[int, float]) -> str:
        _, access_token = AccessJWToken()(user_identifier=str(subject))
        return access_token

    def _create_refresh_token(self, subject: Union[int, float], access_token: Optional[str] = None) -> str:
        if not access_token:
            access_token = self._create_access_token(self.id)
        _, refresh_token = RefreshJWToken()(access_token)
        Token.objects.create(author_id=str(subject),
                             token=refresh_token)
        return refresh_token

    def _generate_jwt_token(self):
        return self._create_access_token(self.id)

    def _generate_refresh_jwt_token(self, access_token: Optional[str] = None):
        if not access_token:
            access_token = self._create_access_token(self.id)
        return self._create_refresh_token(self.id, access_token)

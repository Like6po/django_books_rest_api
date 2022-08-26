import uuid

from django.db import models


class RecoveryCode(models.Model):
    id = models.UUIDField("Идентификатор", primary_key=True, default=uuid.uuid4)
    created_at = models.DateTimeField("Время регистрации", auto_now_add=True)
    user = models.ForeignKey(to="User", on_delete=models.CASCADE, to_field="id")
    is_active = models.BooleanField("Активен ли?", default=True)

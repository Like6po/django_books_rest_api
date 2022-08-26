from django.db import models


class ConfirmCode(models.Model):
    id = models.AutoField("Идентификатор", primary_key=True)
    created_at = models.DateTimeField("Время регистрации", auto_now_add=True)
    user = models.ForeignKey(to="User", on_delete=models.CASCADE, to_field="id")
    is_active = models.BooleanField("Активен ли?", default=True)

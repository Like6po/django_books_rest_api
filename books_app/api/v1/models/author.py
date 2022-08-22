from django.db import models


class Author(models.Model):
    class Meta:
        db_table = "authors"
        ordering = ["id"]
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"

    id = models.AutoField("ID", primary_key=True)
    created_at = models.DateTimeField("Время регистрации", auto_now_add=True)
    first_name = models.CharField("Имя", max_length=128)
    second_name = models.CharField("Фамилия", max_length=128)
    password_hash = models.CharField("Хеш пароля", max_length=256)

    def full_name(self):
        return f"{self.first_name} {self.second_name}"

    full_name.short_description = "Полное имя"

    def __str__(self):
        return f"<ID{self.id} - {self.first_name} {self.second_name}>"

    def is_authenticated(self):
        return True

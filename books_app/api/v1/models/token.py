from django.db import models


class Token(models.Model):
    id = models.AutoField("Идентификатор", primary_key=True)
    author = models.ForeignKey(to="User", on_delete=models.CASCADE, to_field="id")
    token = models.TextField("Токен", unique=True, default=None)
    is_active = models.BooleanField("Активен ли?", default=True)

    def __str__(self):
        return f"<ID{self.id} токен автора: {self.author}>"

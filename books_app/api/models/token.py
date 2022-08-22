from django.db import models


class Token(models.Model):
    uuid = models.UUIDField("UUID", primary_key=True)
    author = models.ForeignKey(to="Author", on_delete=models.CASCADE, to_field="id")
    is_active = models.BooleanField("Активен ли?", default=True)

    def __str__(self):
        return f"<ID{self.id} токен автора: {self.author}>"

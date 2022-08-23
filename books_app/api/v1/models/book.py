from django.db import models


class Book(models.Model):
    class Meta:
        db_table = "books"
        ordering = ["id"]
        verbose_name = "Книга"
        verbose_name_plural = "Книги"

    id = models.AutoField("ID", primary_key=True)
    created_at = models.DateTimeField("Время создания", auto_now_add=True)
    name = models.CharField("Название", max_length=256)
    publish_date = models.DateField("Дата выпуска")
    archived = models.BooleanField("Архивировано", default=False)
    authors = models.ManyToManyField(to="User", blank=True)

    def __str__(self):
        return f"<ID{self.id}- {self.name}>"

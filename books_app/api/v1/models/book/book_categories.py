from django.db import models


class BookCategory(models.Model):
    class Meta:
        db_table = "book_categories"
        ordering = ["id"]
        verbose_name = "Категория книги"
        verbose_name_plural = "Категории книг"

    id = models.AutoField("ID", primary_key=True)
    created_at = models.DateTimeField("Время создания", auto_now_add=True)
    name = models.CharField("Название", max_length=256)

    def value_from_object(self):
        return self.id

    def __str__(self):
        return f"{self.id} - {self.name}"

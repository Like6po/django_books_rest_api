from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class BookRating(models.Model):
    class Meta:
        db_table = "book_ratings"
        ordering = ["id"]
        verbose_name = "Оценка книги"
        verbose_name_plural = "Оценки книг"

    id = models.AutoField("ID", primary_key=True)
    created_at = models.DateTimeField("Время создания", auto_now_add=True)
    value = models.PositiveIntegerField("Значение", validators=[MinValueValidator(1), MaxValueValidator(10)])
    book = models.ForeignKey(to="Book", on_delete=models.CASCADE, to_field="id")
    author = models.ForeignKey(to="User", on_delete=models.CASCADE, to_field="id")

    def __str__(self):
        return f"{self.author} - {self.value}"

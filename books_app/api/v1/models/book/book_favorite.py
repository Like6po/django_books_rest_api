from django.db import models


class BookFavorite(models.Model):
    class Meta:
        db_table = "book_favorite"
        ordering = ["id"]
        verbose_name = "Избранная книга"
        verbose_name_plural = "Избранные книги"

    id = models.AutoField("ID", primary_key=True)
    created_at = models.DateTimeField("Время создания", auto_now_add=True)
    book = models.ForeignKey(to="Book", on_delete=models.CASCADE, to_field="id")
    author = models.ForeignKey(to="User", on_delete=models.CASCADE, to_field="id")

    def __str__(self):
        return f"{self.author} - {self.book}"

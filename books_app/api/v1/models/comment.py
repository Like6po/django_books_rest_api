from django.db import models


class Comment(models.Model):
    class Meta:
        db_table = "comments"
        ordering = ["id"]
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    id = models.AutoField("ID", primary_key=True)
    created_at = models.DateTimeField("Время создания", auto_now_add=True)
    author = models.ForeignKey(to="Author", on_delete=models.CASCADE, to_field="id")
    book = models.ForeignKey(to="Book", on_delete=models.CASCADE, to_field="id")
    text = models.CharField("Текст", max_length=4096)

    def __str__(self):
        return f"<ID{self.id} Коммент к книге: {self.book.name}>"

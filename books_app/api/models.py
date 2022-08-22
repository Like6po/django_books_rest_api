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
    authors = models.ManyToManyField(to="Author", blank=False)

    def __str__(self):
        return f"<ID{self.id}- {self.name}>"


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


class Token(models.Model):
    class TokenType(models.IntegerChoices):
        ACCESS = 0, "access"
        REFRESH = 1, "refresh"

    uuid = models.UUIDField("UUID")
    type = models.SmallIntegerField("Тип (0 - acccess/ 1 - refresh)",
                                    choices=TokenType.choices,
                                    default=TokenType.ACCESS)
    author = models.ForeignKey(to="Author", on_delete=models.CASCADE, to_field="id")
    is_active = models.BooleanField("Активен?", default=True)

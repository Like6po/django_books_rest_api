from django.contrib import admin

from api.v1.models.book import Book
from api.v1.models.comment import Comment
from api.v1.models.token import Token
from api.v1.models.user import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("identifier",)
    list_filter = ("email", "first_name", "second_name", "patronymic")
    search_fields = ("email", "first_name", "second_name", "patronymic")

    def identifier(self, object: User):
        return object.__str__()


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("identifier",)
    list_filter = ("name", "authors__first_name", "authors__second_name", "authors__patronymic")
    search_fields = ("name", "authors__first_name", "authors__second_name", "authors__patronymic")

    def identifier(self, object: Book):
        return object.__str__()


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass


@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    pass

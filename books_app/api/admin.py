from django.contrib import admin

from api.v1.models.author import Author
from api.v1.models.book import Book
from api.v1.models.comment import Comment
from api.v1.models.token import Token


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    pass


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass


@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    pass

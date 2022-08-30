from django.contrib import admin

from api.v1.models.book.book import Book
from api.v1.models.book.book_categories import BookCategory
from api.v1.models.book.book_favorite import BookFavorite
from api.v1.models.book.book_rating import BookRating
from api.v1.models.book.comment import Comment
from api.v1.models.confirm_code import ConfirmCode
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
    list_filter = ("name", "authors__first_name", "authors__second_name", "authors__patronymic", "category__name")
    search_fields = ("name", "authors__first_name", "authors__second_name", "authors__patronymic", "category__name")

    def identifier(self, object: Book):
        return object.__str__()


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass


@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    pass


@admin.register(ConfirmCode)
class ConfirmCodeAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "created_at", "is_active")


@admin.register(BookCategory)
class BookCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(BookRating)
class BookRatingAdmin(admin.ModelAdmin):
    pass


@admin.register(BookFavorite)
class BookFavoriteAdmin(admin.ModelAdmin):
    pass

from django.db.models import Q, Avg, Exists, OuterRef
from django.db.models.functions import Coalesce
from rest_framework import status

from api.v1.consts import StatusValues
from api.v1.models.book.book import Book
from api.v1.models.book.book_favorite import BookFavorite
from api.v1.serializers.book.book import BooksSerializer, BookSerializer
from api.v1.services.base import BaseService
from api.v1.services.misc import value_to_type_or_none


class BookService(BaseService):
    def get_all(self) -> dict:
        try:
            search_name = value_to_type_or_none(self.request.GET.get("name", None), str)
            search_author = value_to_type_or_none(self.request.GET.get("author", None), str)
            search_category = value_to_type_or_none(self.request.GET.get("category", None), int)
            filter_rating_max = value_to_type_or_none(self.request.GET.get("rating_max", None), int)
            filter_rating_min = value_to_type_or_none(self.request.GET.get("rating_min", None), int)
            is_sort_by_rating = value_to_type_or_none(self.request.GET.get("sort_by_rating", None), bool)
            is_sort_by_category = value_to_type_or_none(self.request.GET.get("sort_by_category", None), bool)
        except ValueError as e:
            return {"detail": e.args,
                    "status": StatusValues.FAILED.value,
                    "status_code": status.HTTP_400_BAD_REQUEST}

        books = Book.objects.filter(archived=False)
        books = books.annotate(rating=Coalesce(Avg("bookrating__value"), 0.0))
        books = books.annotate(is_favorite=Exists(BookFavorite.objects.filter(author=self.request.user,
                                                                              book__id=OuterRef("pk"))))

        if is_sort_by_rating:
            books = books.order_by("-rating")
        if is_sort_by_category:
            books = books.order_by("category")
        if search_name:
            books = books.filter(name__contains=search_name)
        if search_author:
            books = books.filter(
                Q(authors__first_name__contains=search_author) |
                Q(authors__second_name__contains=search_author) |
                Q(authors__patronymic__contains=search_author))
        if search_category:
            books = books.filter(category=search_category)
        if filter_rating_max:
            books = books.filter(bookrating__value__lt=filter_rating_max)
        if filter_rating_min:
            books = books.filter(bookrating__value__gt=filter_rating_min)
        serializer = BooksSerializer(instance=books, many=True,
                                     context={"author": self.request.user})

        return {"detail": serializer.data,
                "status": StatusValues.SUCCESS.value,
                "status_code": status.HTTP_200_OK}

    def create(self) -> dict:
        if not (self.request.user.is_author or self.request.user.is_admin):
            return {"detail": "Users can't add books",
                    "status": StatusValues.FAILED.value,
                    "status_code": status.HTTP_403_FORBIDDEN}
        serializer = BooksSerializer(data=self.request.data,
                                     context={'user': self.request.user} if self.request.user.is_author else {})
        if not serializer.is_valid():
            return {"detail": serializer.errors,
                    "status": StatusValues.FAILED.value,
                    "status_code": status.HTTP_400_BAD_REQUEST}

        serializer.save()
        return {"detail": serializer.data,
                "status": StatusValues.SUCCESS.value,
                "status_code": status.HTTP_201_CREATED}

    def get_one(self) -> dict:

        book = Book.objects.filter(id=self.request.parser_context.get("kwargs").get("book_id"))
        book = book.annotate(rating=Coalesce(Avg("bookrating__value"), 0.0))
        book = book.annotate(is_favorite=Exists(BookFavorite.objects.filter(author=self.request.user,
                                                                            book__id=OuterRef("pk"))))
        book = book.first()
        if not book:
            return {"detail": "Book not found",
                    "status": StatusValues.FAILED.value,
                    "status_code": status.HTTP_404_NOT_FOUND}

        serializer = BookSerializer(instance=book,
                                    context={"author": self.request.user})

        return {"detail": serializer.data,
                "status": StatusValues.SUCCESS.value,
                "status_code": status.HTTP_200_OK}

    def delete(self) -> dict:
        if not (self.request.user.is_author or self.request.user.is_admin):
            return {"detail": "Users can't delete books",
                    "status": StatusValues.FAILED.value,
                    "status_code": status.HTTP_403_FORBIDDEN}

        book = Book.objects.filter(id=self.request.parser_context.get("kwargs").get("book_id")).first()
        if not book:
            return {"detail": "Book not found",
                    "status": StatusValues.FAILED.value,
                    "status_code": status.HTTP_404_NOT_FOUND}
        if not (self.request.user.is_admin or self.request.user in book.authors.all()):
            return {"detail": "You can't delete this book",
                    "status": StatusValues.FAILED.value,
                    "status_code": status.HTTP_403_FORBIDDEN}
        book.delete()
        return {"status": StatusValues.SUCCESS.value,
                "status_code": status.HTTP_204_NO_CONTENT}

    def update(self, partial: bool = False) -> dict:
        if not (self.request.user.is_author or self.request.user.is_admin):
            return {"detail": "Users can't edit books",
                    "status": StatusValues.FAILED.value,
                    "status_code": status.HTTP_403_FORBIDDEN}

        book = Book.objects.filter(id=self.request.parser_context.get("kwargs").get("book_id")).first()
        if not book:
            return {"detail": "Book not found",
                    "status": StatusValues.FAILED.value,
                    "status_code": status.HTTP_404_NOT_FOUND}
        if not (self.request.user.is_admin or self.request.user in book.authors.all()):
            return {"detail": "You can't edit this book",
                    "status": StatusValues.FAILED.value,
                    "status_code": status.HTTP_403_FORBIDDEN}
        serializer = BookSerializer(instance=book, data=self.request.data, partial=partial)
        if not serializer.is_valid():
            return {"detail": serializer.errors,
                    "status": StatusValues.FAILED.value,
                    "status_code": status.HTTP_400_BAD_REQUEST}
        serializer.save()
        return {"detail": serializer.data,
                "status": StatusValues.SUCCESS.value,
                "status_code": status.HTTP_200_OK}

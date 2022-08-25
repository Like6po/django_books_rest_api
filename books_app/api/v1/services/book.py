from rest_framework import status

from api.v1.consts import StatusValues
from api.v1.models.book import Book
from api.v1.serializers.book import BooksSerializer, BookSerializer
from api.v1.services.base import BaseService


class BookService(BaseService):
    def get_all(self) -> dict:
        serializer = BooksSerializer(instance=Book.objects.filter(archived=False), many=True)
        return {"detail": {"books": serializer.data},
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
        try:
            book = Book.objects.get(id=self.request.parser_context.get("kwargs").get("book_id"))
        except Book.DoesNotExist:
            return {"detail": "Book not found",
                    "status": StatusValues.FAILED.value,
                    "status_code": status.HTTP_404_NOT_FOUND}
        serializer = BookSerializer(instance=book)
        return {"detail": serializer.data,
                "status": StatusValues.SUCCESS.value,
                "status_code": status.HTTP_200_OK}

    def delete(self) -> dict:
        if not (self.request.user.is_author or self.request.user.is_admin):
            return {"detail": "Users can't delete books",
                    "status": StatusValues.FAILED.value,
                    "status_code": status.HTTP_403_FORBIDDEN}
        try:
            book = Book.objects.get(id=self.request.parser_context.get("kwargs").get("book_id"))
        except Book.DoesNotExist:
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
        try:
            book = Book.objects.get(id=self.request.parser_context.get("kwargs").get("book_id"))
        except Book.DoesNotExist:
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

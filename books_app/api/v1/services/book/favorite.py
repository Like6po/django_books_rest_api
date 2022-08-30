from rest_framework import status

from api.v1.consts import StatusValues
from api.v1.models.book.book import Book
from api.v1.models.book.book_favorite import BookFavorite
from api.v1.serializers.book.favorite import FavoriteBooksSerializer, FavoriteBookIdSerializer
from api.v1.services.base import BaseService


class FavoriteService(BaseService):

    def get_all(self) -> dict:

        favorite = BookFavorite.objects.filter(author=self.request.user)

        serializer = FavoriteBooksSerializer(
            instance=favorite,
            many=True)

        return {"detail": serializer.data,
                "status": StatusValues.SUCCESS.value,
                "status_code": status.HTTP_200_OK}

    def create(self) -> dict:
        serializer = FavoriteBookIdSerializer(data=self.request.data)
        if not serializer.is_valid():
            return {"detail": serializer.errors,
                    "status": StatusValues.FAILED.value,
                    "status_code": status.HTTP_400_BAD_REQUEST}

        book = Book.objects.filter(id=serializer.validated_data.get("book")).first()
        if not book:
            return {"detail": "Book not found",
                    "status": StatusValues.FAILED.value,
                    "status_code": status.HTTP_404_NOT_FOUND}

        favorite = BookFavorite.objects.filter(author=self.request.user, book=book)
        if favorite:
            return {"detail": "Favorite exists",
                    "status": StatusValues.FAILED.value,
                    "status_code": status.HTTP_400_BAD_REQUEST}

        new_favorite = BookFavorite.objects.create(book=book,
                                                   author=self.request.user)
        serializer = FavoriteBooksSerializer(instance=new_favorite)
        return {"detail": serializer.data,
                "status": StatusValues.SUCCESS.value,
                "status_code": status.HTTP_201_CREATED}

    def delete(self) -> dict:
        serializer = FavoriteBookIdSerializer(data=self.request.data)
        if not serializer.is_valid():
            return {"detail": serializer.errors,
                    "status": StatusValues.FAILED.value,
                    "status_code": status.HTTP_400_BAD_REQUEST}

        book = Book.objects.filter(id=serializer.validated_data.get("book")).first()
        if not book:
            return {"detail": "Book not found",
                    "status": StatusValues.FAILED.value,
                    "status_code": status.HTTP_404_NOT_FOUND}

        favorite = BookFavorite.objects.filter(author=self.request.user, book=book)
        if not favorite:
            return {"detail": "Favorite not exists",
                    "status": StatusValues.FAILED.value,
                    "status_code": status.HTTP_400_BAD_REQUEST}

        favorite.delete()
        return {"status": StatusValues.SUCCESS.value,
                "status_code": status.HTTP_204_NO_CONTENT}

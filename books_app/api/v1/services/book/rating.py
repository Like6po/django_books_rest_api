from rest_framework import status

from api.v1.consts import StatusValues
from api.v1.models.book.book import Book
from api.v1.models.book.book_rating import BookRating
from api.v1.serializers.book.rating import BookRatingsSerializer
from api.v1.services.base import BaseService


class RatingService(BaseService):
    def get_all(self) -> dict:

        ratings = BookRating.objects.filter(book_id=self.request.parser_context.get("kwargs").get("book_id"))

        serializer = BookRatingsSerializer(
            instance=ratings,
            many=True)

        return {"detail": serializer.data,
                "status": StatusValues.SUCCESS.value,
                "status_code": status.HTTP_200_OK}

    def create(self) -> dict:

        book = Book.objects.filter(id=self.request.parser_context.get("kwargs").get("book_id")).first()
        if not book:
            return {"detail": "Book not found",
                    "status": StatusValues.FAILED.value,
                    "status_code": status.HTTP_404_NOT_FOUND}

        rating = BookRating.objects.filter(book_id=self.request.parser_context.get("kwargs").get("book_id"),
                                           author_id=self.request.user).first()
        if rating:
            return {"detail": "Rating exists",
                    "status": StatusValues.FAILED.value,
                    "status_code": status.HTTP_409_CONFLICT}

        serializer = BookRatingsSerializer(data=self.request.data,
                                           context={"book": book,
                                                    "author": self.request.user})
        if not serializer.is_valid():
            return {"detail": serializer.errors,
                    "status": StatusValues.FAILED.value,
                    "status_code": status.HTTP_400_BAD_REQUEST}
        serializer.save()
        return {"detail": serializer.data,
                "status": StatusValues.SUCCESS.value,
                "status_code": status.HTTP_201_CREATED}

    def get_one(self) -> dict:

        book = Book.objects.filter(id=self.request.parser_context.get("kwargs").get("book_id")).first()
        if not book:
            return {"detail": "Book not found",
                    "status": StatusValues.FAILED.value,
                    "status_code": status.HTTP_404_NOT_FOUND}
        rating = BookRating.objects.filter(id=self.request.parser_context.get("kwargs").get("rating_id")).first()
        if not rating:
            return {"detail": "Rating not found",
                    "status": StatusValues.FAILED.value,
                    "status_code": status.HTTP_404_NOT_FOUND}

        serializer = BookRatingsSerializer(instance=rating)
        return {"detail": serializer.data,
                "status": StatusValues.SUCCESS.value,
                "status_code": status.HTTP_200_OK}

    def delete(self) -> dict:

        book = Book.objects.filter(id=self.request.parser_context.get("kwargs").get("book_id")).first()
        if not book:
            return {"detail": "Book not found",
                    "status": StatusValues.FAILED.value,
                    "status_code": status.HTTP_404_NOT_FOUND}
        rating = BookRating.objects.filter(id=self.request.parser_context.get("kwargs").get("rating_id")).first()
        if not rating:
            return {"detail": "Rating not found",
                    "status": StatusValues.FAILED.value,
                    "status_code": status.HTTP_404_NOT_FOUND}

        if not (rating.author == self.request.user or
                self.request.user.is_admin):
            return {"detail": "You can't delete this rating",
                    "status": StatusValues.FAILED.value,
                    "status_code": status.HTTP_403_FORBIDDEN}

        rating.delete()
        return {"status": StatusValues.SUCCESS.value,
                "status_code": status.HTTP_204_NO_CONTENT}

    def update(self, partial: bool = False) -> dict:

        book = Book.objects.filter(id=self.request.parser_context.get("kwargs").get("book_id")).first()
        if not book:
            return {"detail": "Book not found",
                    "status": StatusValues.FAILED.value,
                    "status_code": status.HTTP_404_NOT_FOUND}
        rating = BookRating.objects.filter(id=self.request.parser_context.get("kwargs").get("rating_id")).first()
        if not rating:
            return {"detail": "Rating not found",
                    "status": StatusValues.FAILED.value,
                    "status_code": status.HTTP_404_NOT_FOUND}

        if not rating.author == self.request.user:
            return {"detail": "You can't edit this rating",
                    "status": StatusValues.FAILED.value,
                    "status_code": status.HTTP_403_FORBIDDEN}

        serializer = BookRatingsSerializer(instance=rating, data=self.request.data, partial=partial)
        if not serializer.is_valid():
            return {"detail": serializer.errors,
                    "status": StatusValues.FAILED.value,
                    "status_code": status.HTTP_400_BAD_REQUEST}
        serializer.save()
        return {"detail": serializer.data,
                "status": StatusValues.SUCCESS.value,
                "status_code": status.HTTP_200_OK}

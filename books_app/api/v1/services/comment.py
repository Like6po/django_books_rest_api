from rest_framework import status

from api.v1.consts import StatusValues
from api.v1.models.book import Book
from api.v1.models.comment import Comment
from api.v1.serializers.comment import CommentsSerializer, CommentSerializer
from api.v1.services.base import BaseService


class CommentService(BaseService):
    def get_all(self) -> dict:
        serializer = CommentsSerializer(
            instance=Comment.objects.filter(book_id=self.request.parser_context.get("kwargs").get("book_id")),
            many=True)
        return {"detail": {"comments": serializer.data},
                "status": StatusValues.SUCCESS.value,
                "status_code": status.HTTP_200_OK}

    def create(self) -> dict:
        try:
            book = Book.objects.get(id=self.request.parser_context.get("kwargs").get("book_id"))
        except Book.DoesNotExist:
            return {"detail": "Book not found",
                    "status": StatusValues.FAILED.value,
                    "status_code": status.HTTP_404_NOT_FOUND}
        serializer = CommentsSerializer(data=self.request.data, context={"book": book,
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
        try:
            comment = Comment.objects.get(id=self.request.parser_context.get("kwargs").get("comment_id"))
        except Comment.DoesNotExist:
            return {"detail": "Comment not found",
                    "status": StatusValues.FAILED.value,
                    "status_code": status.HTTP_404_NOT_FOUND}
        serializer = CommentSerializer(instance=comment)
        return {"detail": serializer.data,
                "status": StatusValues.SUCCESS.value,
                "status_code": status.HTTP_200_OK}

    def delete(self) -> dict:
        try:
            comment = Comment.objects.get(id=self.request.parser_context.get("kwargs").get("comment_id"))
        except Comment.DoesNotExist:
            return {"detail": "Comment not found",
                    "status": StatusValues.FAILED.value,
                    "status_code": status.HTTP_404_NOT_FOUND}

        if not (comment.author == self.request.user or
                (self.request.user in comment.book.authors.all()) or
                self.request.user.is_admin):
            return {"detail": "You can't delete this comment",
                    "status": StatusValues.FAILED.value,
                    "status_code": status.HTTP_403_FORBIDDEN}

        comment.delete()
        return {"status": StatusValues.SUCCESS.value,
                "status_code": status.HTTP_204_NO_CONTENT}

    def update(self, partial: bool = False) -> dict:
        try:
            comment = Comment.objects.get(id=self.request.parser_context.get("kwargs").get("comment_id"))
        except Comment.DoesNotExist:
            return {"detail": "Comment not found",
                    "status": StatusValues.FAILED.value,
                    "status_code": status.HTTP_404_NOT_FOUND}

        if not (comment.author == self.request.user or self.request.user.is_admin):
            return {"detail": "You can't edit this comment",
                    "status": StatusValues.FAILED.value,
                    "status_code": status.HTTP_403_FORBIDDEN}

        serializer = CommentSerializer(instance=comment, data=self.request.data, partial=partial)
        if not serializer.is_valid():
            return {"detail": serializer.errors,
                    "status": StatusValues.FAILED.value,
                    "status_code": status.HTTP_400_BAD_REQUEST}
        serializer.save()
        return {"detail": serializer.data,
                "status": StatusValues.SUCCESS.value,
                "status_code": status.HTTP_200_OK}

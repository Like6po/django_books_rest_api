from rest_framework import status

from api.v1.consts import StatusValues
from api.v1.models.book.book import Book
from api.v1.models.book.comment import Comment
from api.v1.serializers.book.comment import CommentsSerializer, CommentSerializer
from api.v1.services.base import BaseService


class CommentService(BaseService):
    def get_all(self) -> dict:

        comments = Comment.objects.filter(book_id=self.request.parser_context.get("kwargs").get("book_id"))

        created_at_min = self.request.GET.get("created_at_min", None)
        created_at_max = self.request.GET.get("created_at_max", None)

        if created_at_min:
            comments = comments.filter(created_at__lt=created_at_max)
        if created_at_max:
            comments = comments.filter(created_at__gt=created_at_min)

        serializer = CommentsSerializer(
            instance=comments,
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

        comment = Comment.objects.filter(id=self.request.parser_context.get("kwargs").get("comment_id")).first()
        if not comment:
            return {"detail": "Comment not found",
                    "status": StatusValues.FAILED.value,
                    "status_code": status.HTTP_404_NOT_FOUND}
        serializer = CommentSerializer(instance=comment)
        return {"detail": serializer.data,
                "status": StatusValues.SUCCESS.value,
                "status_code": status.HTTP_200_OK}

    def delete(self) -> dict:

        comment = Comment.objects.filter(id=self.request.parser_context.get("kwargs").get("comment_id")).first()
        if not comment:
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
        comment = Comment.objects.filter(id=self.request.parser_context.get("kwargs").get("comment_id")).first()
        if not comment:
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

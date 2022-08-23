from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api.v1.models.book import Book
from api.v1.models.comment import Comment
from api.v1.permissions import IsOwnerOrReadOnly
from api.v1.serializers.comment import CommentsSerializer, CommentUpdateSerializer, CommentSerializer


class CommentsView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request: Request, book_id: int):

        comments = Comment.objects.filter(book_id=book_id)

        serializer = CommentsSerializer(comments, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request: Request, book_id: int):
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CommentsSerializer(data=request.data, context={"book": book,
                                                                    "author": request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class CommentView(APIView):
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly]

    def get(self, request: Request, book_id: int, comment_id: int):
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            comment = book.comment_set.get(id=comment_id)
        except Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CommentSerializer(instance=comment, context={'request': request})
        return Response(serializer.data)

    def delete(self, request: Request, book_id: int, comment_id: int):
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            comment = book.comment_set.get(id=comment_id)
        except Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        comment.delete()
        return Response(status=status.HTTP_200_OK)

    def patch(self, request: Request, book_id: int, comment_id: int):
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            comment = book.comment_set.get(id=comment_id)
        except Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CommentUpdateSerializer(data=request.data, instance=comment)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

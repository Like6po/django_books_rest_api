from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models.book import Book
from api.models.comment import Comment
from api.permissions import IsOwnerOrReadOnly
from api.serializers import BookSerializer, BookManualSerializer


class BooksView(APIView):
    serializer_class = BookManualSerializer

    def get(self, request: Request):
        books = Book.objects.filter(archived=False)

        return Response(
            [{"id": book.id, "name": book.name,
              "authors": [{"author_id": author.id, "author_full_name": author.full_name()}
                          for author in book.authors.all()]}
             for book in books])

    def post(self, request: Request):
        serializer = BookManualSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.validated_data)


class BookView(APIView):
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get(self, request: Request, book_id: int):
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        comments = Comment.objects.filter(book=book.id)
        return Response({"id": book.id,
                         "name": book.name,
                         "publish_date": book.publish_date,
                         "comments": [{"id": comment.id,
                                       "text": comment.text,
                                       "author": {"id": comment.author.id,
                                                  "full_name": comment.author.full_name()}}
                                      for comment in comments.all()]})

    def delete(self, request: Request, book_id: int):
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        book.delete()
        return Response(status=status.HTTP_200_OK)

    def put(self, request: Request, book_id):
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = BookManualSerializer(data=request.data, instance=book)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data)

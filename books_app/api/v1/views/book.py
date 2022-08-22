from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api.v1.models.book import Book
from api.v1.models.comment import Comment
from api.v1.permissions import IsOwnerOrReadOnly
from api.v1.serializers.book import BooksSerializer, BookSerializer


class BooksView(APIView):
    serializer_class = BooksSerializer

    def get(self, request: Request):
        books = Book.objects.filter(archived=False)
        serializer = BooksSerializer(books, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request: Request):
        serializer = BooksSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


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
        serializer = BookSerializer(data=request.data, instance=book)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data)

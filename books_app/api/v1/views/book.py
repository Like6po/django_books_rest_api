from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api.v1.models.book import Book
from api.v1.serializers.book import BooksSerializer, BookSerializer, BookUpdateSerializer


class BooksView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request: Request):
        books = Book.objects.filter(archived=False)
        serializer = BooksSerializer(books, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request: Request):
        serializer = BooksSerializer(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class BookView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request: Request, book_id: int):
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = BookSerializer(book, context={'request': request})
        return Response(serializer.data)

    def delete(self, request: Request, book_id: int):
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        book.delete()
        return Response(status=status.HTTP_200_OK)

    def patch(self, request: Request, book_id):
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = BookUpdateSerializer(data=request.data, instance=book)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

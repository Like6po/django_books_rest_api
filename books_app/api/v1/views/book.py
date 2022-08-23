from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api.v1.models.book import Book
from api.v1.serializers.book import BooksSerializer, BookSerializer, BookUpdateSerializer


class BooksView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        books = Book.objects.filter(archived=False)
        serializer = BooksSerializer(books, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request: Request):
        if not (request.user.is_author or request.user.is_admin):
            return Response({"detail": "Users can't add books"}, status=status.HTTP_403_FORBIDDEN)
        serializer = BooksSerializer(data=request.data,
                                     context={'user': request.user} if request.user.is_author else {})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class BookView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, book_id: int):
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = BookSerializer(book, context={'request': request})
        return Response(serializer.data)

    def delete(self, request: Request, book_id: int):
        if not (request.user.is_author or request.user.is_admin):
            return Response({"detail": "Users can't delete books"}, status=status.HTTP_403_FORBIDDEN)
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if not (request.user.is_admin or request.user in book.authors.all()):
            return Response({"detail": "You can't delete this book"}, status=status.HTTP_403_FORBIDDEN)
        book.delete()
        self.check_object_permissions(self.request, book)
        return Response(status=status.HTTP_200_OK)

    def patch(self, request: Request, book_id):
        if not (request.user.is_author or request.user.is_admin):
            return Response({"detail": "Users can't edit books"}, status=status.HTTP_403_FORBIDDEN)
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if not (request.user.is_admin or request.user in book.authors.all()):
            return Response({"detail": "You can't edit this book"}, status=status.HTTP_403_FORBIDDEN)
        serializer = BookUpdateSerializer(data=request.data, instance=book)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

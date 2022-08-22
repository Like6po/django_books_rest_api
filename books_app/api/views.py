from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Author, Book, Comment
from api.permissions import IsOwnerOrReadOnly
from api.security import create_access_token, create_refresh_token
from api.serializers import BookSerializer, RegisterAuthorSerializer, \
    LoginAuthorSerializer, RefreshAuthorSerializer


class RegisterView(APIView):
    serializer_class = RegisterAuthorSerializer

    def post(self, request: Request):
        serializer = RegisterAuthorSerializer(data=request.data)
        if serializer.is_valid():
            author: Author = serializer.create(serializer.validated_data)
            return Response({"id": author.id,
                             "full_name": author.full_name(),
                             }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    serializer_class = LoginAuthorSerializer

    def post(self, request: Request):
        serializer = LoginAuthorSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        access_token = create_access_token(str(serializer.validated_data["author_id"]))[1]
        refresh_token = create_refresh_token(str(serializer.validated_data["author_id"]))[1]
        return Response({"access_token": access_token,
                         "refresh_token": refresh_token}, status=200)


class RefreshView(APIView):
    serializer_class = RefreshAuthorSerializer

    def post(self, request: Request):
        serializer = RefreshAuthorSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        access_token = create_access_token(str(serializer.token.sub))[1]
        refresh_token = create_refresh_token(str(serializer.token.sub))[1]
        return Response({"access_token": access_token,
                         "refresh_token": refresh_token}, status=200)


class AuthorsView(APIView):
    def get(self, request: Request):
        authors = Author.objects.all()
        return Response(
            [{"id": author.id, "full_name": author.full_name(),
              "books": [{"id": book.id, "name": book.name}
                        for book in author.book_set.all()]}
             for author in authors])


class BooksView(APIView):
    serializer_class = BookSerializer

    def get(self, request: Request):
        books = Book.objects.filter(archived=False)

        return Response(
            [{"id": book.id, "name": book.name,
              "authors": [{"author_id": author.id, "author_full_name": author.full_name()}
                          for author in book.authors.all()]}
             for book in books])

    def post(self, request: Request):
        serializer = BookSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        new_book = Book.objects.create(**serializer.validated_data)
        return Response({"id": new_book.id, "name": new_book.name})


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
        serializer = BookSerializer(book)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        book = Book.objects.filter(id=book_id).update(**request.data)
        return Response({"id": book.id,
                         "name": book.name,
                         "publish_date": book.publish_date})

from rest_framework import permissions, status
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Author, Book, Comment
from api.permissions import IsOwnerOrReadOnly
from api.security import create_access_token, create_refresh_token
from api.serializers import AuthorSerializer, BookSerializer, CommentSerializer, RegisterAuthorSerializer, \
    LoginAuthorSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all().order_by('-created_at')
    serializer_class = AuthorSerializer
    permission_classes = []


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


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

    def get(self, request: Request):
        serializer = LoginAuthorSerializer(data=request.query_params.dict())
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        #
        # Хотел сделать хранение токенов в бд,
        # чтобы выдавать при повторыном обращении тот же токен, что и в прошлый раз
        #
        # try:
        #     access_token = Token.objects.get(author_id=serializer.validated_data["author_id"],
        #                                      type=Token.TokenType.ACCESS.value,
        #                                      is_active=True)
        #     refresh_token = Token.objects.get(author_id=serializer.validated_data["author_id"],
        #                                       type=Token.TokenType.REFRESH.value,
        #                                       is_active=True)
        # except Token.DoesNotExist:
        #     access_token = create_access_token(serializer.validated_data["author_id"])
        #     refresh_token = create_refresh_token(serializer.validated_data["author_id"])
        #     Token.objects.filter(author_id=access_token[0].sub).update(is_active=False)
        #     Token.objects.create(uuid=access_token[0].jti,
        #                          type=[token_type[0]
        #                                for token_type in Token.TokenType.choices if
        #                                token_type[1] == access_token[0].type][0],
        #                          author_id=access_token[0].sub)
        #     Token.objects.create(uuid=refresh_token[0].jti,
        #                          type=[token_type[0]
        #                                for token_type in Token.TokenType.choices if
        #                                token_type[1] == refresh_token[0].type][0],
        #                          author_id=refresh_token[0].sub)
        #     access_token = access_token[1]
        #     refresh_token = refresh_token[1]

        access_token = create_access_token(serializer.validated_data["author_id"])[1]
        refresh_token = create_refresh_token(serializer.validated_data["author_id"])[1]
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

    def update(self, request: Request, book_id):
        book = Book.objects.filter(id=book_id).update(**request.data)
        return Response({"id": book.id,
                         "name": book.name,
                         "publish_date": book.publish_date})

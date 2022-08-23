from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api.v1.models.author import Author
from api.v1.serializers.author import AuthorsSerializer


class AuthorsView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request: Request):
        authors = Author.objects.all()
        serializer = AuthorsSerializer(instance=authors, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request: Request):
        serializer = AuthorsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class AuthorView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request: Request, author_id: int):
        try:
            book = Author.objects.get(id=author_id)
        except Author.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = AuthorsSerializer(book, context={'request': request})
        return Response(serializer.data)

    def delete(self, request: Request, author_id: int):
        try:
            author = Author.objects.get(id=author_id)
        except Author.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        author.delete()
        return Response(status=status.HTTP_200_OK)

    def patch(self, request: Request, author_id):
        try:
            author = Author.objects.get(id=author_id)
        except Author.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = AuthorsSerializer(data=request.data, instance=author)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

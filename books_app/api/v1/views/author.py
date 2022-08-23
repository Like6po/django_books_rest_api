from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api.v1.models.user import User
from api.v1.serializers.author import AuthorsSerializer


class AuthorsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        authors = User.objects.filter(role=User.ROLES.AUTHOR.value)
        serializer = AuthorsSerializer(instance=authors, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request: Request):
        if not request.user.is_admin:
            return Response({"detail": "Only admins can create authors"}, status=status.HTTP_403_FORBIDDEN)
        serializer = AuthorsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class AuthorView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, author_id: int):
        try:
            book = User.objects.get(id=author_id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = AuthorsSerializer(book, context={'request': request})
        return Response(serializer.data)

    def delete(self, request: Request, author_id: int):
        if not request.user.is_admin:
            return Response({"detail": "Only admins can delete another accounts"}, status=status.HTTP_403_FORBIDDEN)
        try:
            author = User.objects.get(id=author_id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        author.delete()
        return Response(status=status.HTTP_200_OK)

    def patch(self, request: Request, author_id):
        if not (request.user.is_admin or request.user.id == author_id):
            return Response({"detail": "Only admins can change another accounts"}, status=status.HTTP_403_FORBIDDEN)
        try:
            author = User.objects.get(id=author_id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = AuthorsSerializer(data=request.data, instance=author)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

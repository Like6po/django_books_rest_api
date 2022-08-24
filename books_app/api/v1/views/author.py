from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from api.v1.models.user import User
from api.v1.serializers.author import AuthorsSerializer, AuthorsUpdateSerializer


class AuthorsView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = AuthorsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(role=User.ROLES.AUTHOR.value)

    def create(self, request: Request, *args, **kwargs):
        if not request.user.is_admin:
            return Response({"detail": "Only admins can create authors"}, status=status.HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)


class AuthorView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = AuthorsUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        queryset = self.get_queryset()
        return get_object_or_404(queryset, id=self.kwargs["author_id"], role=User.ROLES.AUTHOR.value)

    def delete(self, request: Request, *args, **kwargs):
        if not request.user.is_admin:
            return Response({"detail": "Only admins can delete accounts"}, status=status.HTTP_403_FORBIDDEN)
        return super().delete(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if not (request.user.is_admin or request.user.id == kwargs['author_id']):
            return Response({"detail": "Only admins can change another accounts"}, status=status.HTTP_403_FORBIDDEN)
        if request.user.id == kwargs["author_id"]:
            return Response({"detail": "Cant delete self account"}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def patch(self, request: Request, *args, **kwargs):
        if not (request.user.is_admin or request.user.id == kwargs['author_id']):
            return Response({"detail": "Only admins can change another accounts"}, status=status.HTTP_403_FORBIDDEN)
        return super().patch(request, *args, **kwargs)

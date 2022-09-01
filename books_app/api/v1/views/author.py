from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from api.v1.serializers.author import AuthorsSerializer
from api.v1.services.author import AuthorService


class AuthorsView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AuthorsSerializer

    def get(self, request: Request, *args, **kwargs):
        author = AuthorService(request)
        result = author.get_all()
        return Response(result, status=result["status_code"])

    def create(self, request: Request, *args, **kwargs):
        author = AuthorService(request)
        result = author.create()
        return Response(result, status=result["status_code"])


class AuthorView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AuthorsSerializer

    def get(self, request: Request, *args, **kwargs):
        author = AuthorService(request)
        result = author.get_one()
        return Response(result, status=result["status_code"])

    def delete(self, request: Request, *args, **kwargs):
        author = AuthorService(request)
        result = author.delete()
        return Response(result, status=result["status_code"])

    def update(self, request, *args, **kwargs):
        author = AuthorService(request)
        result = author.update()
        return Response(result, status=result["status_code"])

    def patch(self, request: Request, *args, **kwargs):
        author = AuthorService(request)
        result = author.update(partial=True)
        return Response(result, status=result["status_code"])

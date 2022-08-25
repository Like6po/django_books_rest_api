from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from api.v1.services.book import BookService


class BooksView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, *args, **kwargs):
        book = BookService(request)
        result = book.get_all()
        return Response(result, status=result["status_code"])

    def create(self, request: Request, *args, **kwargs):
        book = BookService(request)
        result = book.create()
        return Response(result, status=result["status_code"])


class BookView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, *args, **kwargs):
        book = BookService(request)
        result = book.get_one()
        return Response(result, status=result["status_code"])

    def delete(self, request: Request, *args, **kwargs):
        book = BookService(request)
        result = book.delete()
        return Response(result, status=result["status_code"])

    def update(self, request, *args, **kwargs):
        book = BookService(request)
        result = book.update()
        return Response(result, status=result["status_code"])

    def patch(self, request: Request, *args, **kwargs):
        book = BookService(request)
        result = book.update(partial=True)
        return Response(result, status=result["status_code"])

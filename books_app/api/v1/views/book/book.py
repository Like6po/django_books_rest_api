from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from api.v1.serializers.book.book import BooksSerializer, BookSerializer
from api.v1.services.book.book import BookService


class BooksView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BooksSerializer

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('name',
                          openapi.IN_QUERY,
                          "Поиск по имени книги",
                          type=openapi.TYPE_STRING),
        openapi.Parameter("author",
                          openapi.IN_QUERY,
                          "Поиск по ФИО автора",
                          type=openapi.TYPE_STRING),
        openapi.Parameter("category",
                          openapi.IN_QUERY,
                          "Фильтр по категории",
                          type=openapi.TYPE_INTEGER),
        openapi.Parameter("rating_max",
                          openapi.IN_QUERY,
                          "Максимальный рейтинг",
                          type=openapi.TYPE_INTEGER),
        openapi.Parameter("rating_min",
                          openapi.IN_QUERY,
                          "Минимальный рейтинг",
                          type=openapi.TYPE_INTEGER),
        openapi.Parameter("sort_by_rating",
                          openapi.IN_QUERY,
                          "Сортировка по рейтингу",
                          type=openapi.TYPE_BOOLEAN),
        openapi.Parameter("sort_by_category",
                          openapi.IN_QUERY,
                          "Сортировка по категории",
                          type=openapi.TYPE_BOOLEAN)
    ])
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
    serializer_class = BookSerializer

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

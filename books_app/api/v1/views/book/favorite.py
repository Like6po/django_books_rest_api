from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from api.v1.services.book.favorite import FavoriteService


class RatingsView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, *args, **kwargs):
        rating = FavoriteService(request)
        result = rating.get_all()
        return Response(result, status=result["status_code"])

    def create(self, request: Request, *args, **kwargs):
        rating = FavoriteService(request)
        result = rating.create()
        return Response(result, status=result["status_code"])

    def delete(self, request: Request, *args, **kwargs):
        rating = FavoriteService(request)
        result = rating.delete()
        return Response(result, status=result["status_code"])

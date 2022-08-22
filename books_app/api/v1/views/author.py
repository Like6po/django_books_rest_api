from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api.v1.models.author import Author


class AuthorsView(APIView):
    def get(self, request: Request):
        authors = Author.objects.all()
        return Response(
            [{"id": author.id, "full_name": author.full_name(),
              "books": [{"id": book.id, "name": book.name}
                        for book in author.book_set.all()]}
             for author in authors])

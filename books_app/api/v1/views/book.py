from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from api.v1.models.book import Book
from api.v1.serializers.book import BooksSerializer, BookSerializer


class BooksView(ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BooksSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(archived=False)

    def create(self, request: Request, *args, **kwargs):
        if not (request.user.is_author or request.user.is_admin):
            return Response({"detail": "Users can't add books"}, status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(data=request.data,
                                         context={'user': request.user} if request.user.is_author else {})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class BookView(RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        queryset = self.get_queryset()
        return get_object_or_404(queryset, id=self.kwargs["book_id"])

    def delete(self, request: Request, *args, **kwargs):
        if not (request.user.is_author or request.user.is_admin):
            return Response({"detail": "Users can't delete books"}, status=status.HTTP_403_FORBIDDEN)
        if not (request.user.is_admin or request.user in self.get_object().authors.all()):
            return Response({"detail": "You can't delete this book"}, status=status.HTTP_403_FORBIDDEN)
        return super().delete(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if not (request.user.is_author or request.user.is_admin):
            return Response({"detail": "Users can't edit books"}, status=status.HTTP_403_FORBIDDEN)
        if not (request.user.is_admin or request.user in self.get_object().authors.all()):
            return Response({"detail": "You can't edit this book"}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def patch(self, request: Request, *args, **kwargs):
        if not (request.user.is_author or request.user.is_admin):
            return Response({"detail": "Users can't edit books"}, status=status.HTTP_403_FORBIDDEN)
        if not (request.user.is_admin or request.user in self.get_object().authors.all()):
            return Response({"detail": "You can't edit this book"}, status=status.HTTP_403_FORBIDDEN)
        return super().patch(request, *args, **kwargs)

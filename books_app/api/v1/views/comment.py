from rest_framework import status
from rest_framework.generics import ListCreateAPIView, get_object_or_404, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from api.v1.models.book import Book
from api.v1.models.comment import Comment
from api.v1.serializers.comment import CommentsSerializer, CommentSerializer


class CommentsView(ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentsSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(queryset=Book.objects.all(), id=self.kwargs["book_id"])

    def get_queryset(self):
        return self.queryset.filter(book_id=self.kwargs["book_id"])

    def create(self, request: Request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"book": self.get_object(),
                                                                     "author": request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class CommentView(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        queryset = self.get_queryset()
        return get_object_or_404(queryset, id=self.kwargs["comment_id"])

    def delete(self, request: Request, *args, **kwargs):
        if not (self.get_object().author == request.user or
                (request.user in self.get_object().book.authors.all()) or
                request.user.is_admin):
            return Response({"detail": "You can't delete this comment"}, status=status.HTTP_403_FORBIDDEN)
        return super().delete(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if not (self.get_object().author == request.user or request.user.is_admin):
            return Response({"detail": "You can't edit this comment"}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def patch(self, request: Request, *args, **kwargs):
        if not (self.get_object().author == request.user or request.user.is_admin):
            return Response({"detail": "You can't edit this comment"}, status=status.HTTP_403_FORBIDDEN)
        return super().patch(request, *args, **kwargs)

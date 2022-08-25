from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from api.v1.services.comment import CommentService


class CommentsView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, *args, **kwargs):
        comment = CommentService(request)
        result = comment.get_all()
        return Response(result, status=result["status_code"])

    def create(self, request: Request, *args, **kwargs):
        comment = CommentService(request)
        result = comment.create()
        return Response(result, status=result["status_code"])


class CommentView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, *args, **kwargs):
        comment = CommentService(request)
        result = comment.get_one()
        return Response(result, status=result["status_code"])

    def delete(self, request: Request, *args, **kwargs):
        comment = CommentService(request)
        result = comment.delete()
        return Response(result, status=result["status_code"])

    def update(self, request, *args, **kwargs):
        comment = CommentService(request)
        result = comment.update()
        return Response(result, status=result["status_code"])

    def patch(self, request: Request, *args, **kwargs):
        comment = CommentService(request)
        result = comment.update(partial=True)
        return Response(result, status=result["status_code"])

from rest_framework import status, serializers

from api.v1.consts import StatusValues
from api.v1.models.user import User
from api.v1.serializers.author import AuthorsSerializer, AuthorsUpdateSerializer
from api.v1.services.base import BaseService


class AuthorService(BaseService):
    def get_all(self) -> dict:
        serializer = AuthorsSerializer(instance=User.objects.filter(role=User.ROLES.AUTHOR.value), many=True)
        return {"detail": serializer.data,
                "status": StatusValues.SUCCESS.value,
                "status_code": status.HTTP_200_OK}

    def create(self) -> dict:
        if not self.request.user.is_admin:
            return {"detail": "Only admins can create authors",
                    "status": StatusValues.FAILED.value,
                    "status_code": status.HTTP_403_FORBIDDEN}
        serializer = AuthorsSerializer(data=self.request.data)
        if not serializer.is_valid():
            return {"detail": serializer.errors,
                    "status": StatusValues.FAILED.value,
                    "status_code": status.HTTP_400_BAD_REQUEST}
        try:
            serializer.save()
        except serializers.ValidationError as e:
            return {"detail": e.detail.pop(),
                    "status": StatusValues.FAILED.value,
                    "status_code": status.HTTP_409_CONFLICT}
        return {"detail": serializer.data,
                "status": StatusValues.SUCCESS.value,
                "status_code": status.HTTP_201_CREATED}

    def get_one(self) -> dict:

        author = User.objects.filter(id=self.request.parser_context.get("kwargs").get("author_id"),
                                     role=User.ROLES.AUTHOR.value).first()
        if not author:
            return {"detail": "Author not found",
                    "status": StatusValues.FAILED.value,
                    "status_code": status.HTTP_404_NOT_FOUND}
        serializer = AuthorsSerializer(instance=author)
        return {"detail": serializer.data,
                "status": StatusValues.SUCCESS.value,
                "status_code": status.HTTP_200_OK}

    def delete(self) -> dict:
        if not self.request.user.is_admin:
            return {"detail": "Only admins can delete accounts",
                    "status": StatusValues.FAILED.value,
                    "status_code": status.HTTP_403_FORBIDDEN}
        if self.request.user.id == self.request.query_params["author_id"]:
            return {"detail": "Cant delete self account",
                    "status": StatusValues.FAILED.value,
                    "status_code": status.HTTP_403_FORBIDDEN}

        author = User.objects.filter(id=self.request.parser_context.get("kwargs").get("author_id"),
                                     role=User.ROLES.AUTHOR.value).first()
        if not author:
            return {"detail": "Author not found",
                    "status": StatusValues.FAILED.value,
                    "status_code": status.HTTP_404_NOT_FOUND}
        author.delete()
        return {"status": StatusValues.SUCCESS.value,
                "status_code": status.HTTP_204_NO_CONTENT}

    def update(self, partial: bool = False) -> dict:
        if not (self.request.user.is_admin or
                self.request.user.id == self.request.parser_context.get("kwargs").get("author_id")):
            return {"detail": "Only admins can change another accounts",
                    "status": StatusValues.FAILED.value,
                    "status_code": status.HTTP_403_FORBIDDEN}

        author = User.objects.filter(id=self.request.parser_context.get("kwargs").get("author_id"),
                                     role=User.ROLES.AUTHOR.value).first()
        if not author:
            return {"detail": "Author not found",
                    "status": StatusValues.FAILED.value,
                    "status_code": status.HTTP_404_NOT_FOUND}
        serializer = AuthorsUpdateSerializer(instance=author, data=self.request.data, partial=partial)
        if not serializer.is_valid():
            return {"detail": serializer.errors,
                    "status": StatusValues.FAILED.value,
                    "status_code": status.HTTP_400_BAD_REQUEST}
        serializer.save()
        return {"detail": serializer.data,
                "status": StatusValues.SUCCESS.value,
                "status_code": status.HTTP_200_OK}

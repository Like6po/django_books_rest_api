from django.core.handlers.wsgi import WSGIRequest
from rest_framework import HTTP_HEADER_ENCODING
from rest_framework.authentication import BasicAuthentication

from api.models import Author
from api.schemas import TokenStruct
from api.security import parse_token_by_type


class JWTAuthentication(BasicAuthentication):

    def authenticate(self, request: WSGIRequest):
        if not request.POST:
            return None
        if not (header := self.get_token_header(request)):
            return None
        if not (token_raw := self.parse_token(header)):
            return None
        if not (token := self.validate_token(token_raw)):
            return None

        user = Author.objects.get(id=token.sub)
        return user, token

    def get_token_header(self, request) -> str:
        token = request.META.get("Authorization")

        if isinstance(token, str):
            token = token.encode(HTTP_HEADER_ENCODING)

        return token

    def parse_token(self, data) -> str | None:
        token_data = data.split()

        if len(token_data) != 2:
            return None

        if token_data[0] != "bearer":
            # Assume the header does not contain a JSON web token
            return None

        return token_data[1]

    def validate_token(self, raw_token) -> TokenStruct | None:
        if not (token := parse_token_by_type(raw_token, "access")):
            return None
        return token

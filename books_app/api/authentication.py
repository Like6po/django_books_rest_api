from typing import Optional

from django.core.handlers.wsgi import WSGIRequest
from rest_framework.authentication import BasicAuthentication

from api.models import Author
from api.schemas import TokenStruct
from api.security import parse_token_by_type


class JWTAuthentication(BasicAuthentication):

    def authenticate(self, request: WSGIRequest):

        if not (header := self.get_token_header(request)):
            return None
        if not (token_raw := self.parse_token(header)):
            return None
        if not (token := self.validate_token(token_raw)):
            return None

        user = Author.objects.get(id=token.sub)
        return user, token

    def get_token_header(self, request) -> str:
        token = request.headers.get("Authorization")
        return token

    def parse_token(self, data) -> Optional[str]:
        token_data = data.split()
        if len(token_data) != 2:
            return None

        if token_data[0] != "Bearer":
            # Assume the header does not contain a JSON web token
            return None

        return token_data[1]

    def validate_token(self, raw_token) -> Optional[TokenStruct]:
        if not (token := parse_token_by_type(raw_token, "access")):
            return None
        return token

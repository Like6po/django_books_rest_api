from typing import Optional

from django.core.handlers.wsgi import WSGIRequest
from rest_framework.authentication import BasicAuthentication

from api.v1.models.user import User
from api.v1.token import AccessJWToken


class JWTAuthentication(BasicAuthentication):

    def authenticate(self, request: WSGIRequest):

        if not (header := self.get_token_header(request)):
            return None
        if not (token_raw := self.parse_token(header)):
            return None
        if not (token := self.validate_token(token_raw)):
            return None
        try:
            user = User.objects.get(id=token.get("sub"))
        except User.DoesNotExist:
            return None
        if not user.is_active:
            return None
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

    def validate_token(self, raw_token) -> Optional[AccessJWToken]:
        try:
            token = AccessJWToken(raw_token)
        except ValueError:
            return None
        return token

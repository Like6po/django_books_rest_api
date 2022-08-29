import abc
from datetime import datetime, timedelta
from enum import Enum
from typing import Optional

from jose import jwt, ExpiredSignatureError, JWTError

from books_app.settings import JWT_ACCESS_TOKEN_EXPIRE_MINUTES, JWT_REFRESH_TOKEN_EXPIRE_DAYS, JWT_ALGORITHM, SECRET_KEY


class TokenTypes(Enum):
    ACCESS = 'access'
    REFRESH = 'refresh'


class JWToken(metaclass=abc.ABCMeta):
    type: Optional[TokenTypes] = None
    lifetime_minutes: Optional[int] = None

    def __init__(self, token: Optional[str] = None):
        self.token = token
        if not self.type or not self.lifetime_minutes:
            raise NotImplementedError
        if not token:
            self.payload = {"type": self.type}
        else:
            if not self.verify():
                raise ValueError("Incorrect token")

    def __call__(self, **kwargs):
        if not self.type or not self.lifetime_minutes:
            raise NotImplementedError
        self.set_type()
        self.set_iat()
        self.set_exp()

    def __repr__(self):
        return str(self.payload)

    def __getitem__(self, key):
        return self.payload[key]

    def __setitem__(self, key, value):
        self.payload[key] = value

    def __delitem__(self, key):
        del self.payload[key]

    def __contains__(self, key):
        return key in self.payload

    def get(self, key, default=None):
        return self.payload.get(key, default)

    def verify(self):
        if not self.token:
            return False
        try:
            payload = jwt.decode(self.token, SECRET_KEY, algorithms=JWT_ALGORITHM)
        except ExpiredSignatureError:
            return False
        except JWTError:
            return False
        self.payload = payload
        return True

    def check_exp(self):
        if not self.token:
            return False
        if not self.payload["exp"]:
            return False
        if datetime.utcnow() - self.payload["exp"] > timedelta(minutes=self.lifetime_minutes):
            return False
        return True

    def check_type(self):
        if not self.token:
            return False
        if not self.payload["type"]:
            return False
        if self.payload["type"] != self.type:
            return False

    def set_exp(self):
        self.payload["exp"] = datetime.utcnow() + timedelta(minutes=self.lifetime_minutes)

    def set_jti(self, jti):
        self.payload["jti"] = jti

    def set_sub(self, sub):
        self.payload["sub"] = sub

    def set_iat(self):
        self.payload["iat"] = datetime.utcnow()

    def set_type(self):
        self.payload["type"] = self.type


class AccessJWToken(JWToken):
    type = TokenTypes.ACCESS.value
    lifetime_minutes = JWT_ACCESS_TOKEN_EXPIRE_MINUTES

    def __call__(self, user_identifier: str):
        super().__call__()
        self.set_sub(user_identifier)
        token = jwt.encode(self.payload, SECRET_KEY, algorithm=JWT_ALGORITHM)
        return self.payload, token


class RefreshJWToken(JWToken):
    type = TokenTypes.REFRESH.value
    lifetime_minutes = JWT_REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60

    def __call__(self):
        super().__call__()
        token = jwt.encode(self.payload, SECRET_KEY, algorithm=JWT_ALGORITHM)
        return self.payload, token

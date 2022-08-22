import uuid
from datetime import datetime, timedelta

from jose import jwt, ExpiredSignatureError

from api.schemas import TokenStruct
from books_app.settings import REFRESH_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES


def create_refresh_token(user_identifier: str) -> tuple[TokenStruct, str]:
    expire_refresh_token = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    refresh_token = TokenStruct(type="refresh",
                                exp=expire_refresh_token,
                                sub=str(user_identifier),
                                jti=str(uuid.uuid4()),
                                iat=datetime.utcnow()
                                )
    refresh_token_encoded = jwt.encode(refresh_token.dict(), SECRET_KEY, algorithm="HS256")
    return refresh_token, refresh_token_encoded


def create_access_token(user_identifier: str) -> tuple[TokenStruct, str]:
    expire_access_token = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = TokenStruct(type="access",
                               exp=expire_access_token,
                               sub=str(user_identifier),
                               jti=str(uuid.uuid4()),
                               iat=datetime.utcnow())
    access_token_encoded = jwt.encode(access_token.dict(), SECRET_KEY, algorithm="HS256")
    return access_token, access_token_encoded


def parse_token(token: str) -> TokenStruct | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms="HS256")
        if payload.get("sub") is None:
            return None
    except ExpiredSignatureError:
        return None

    return TokenStruct(**payload)


def parse_token_by_type(token: str, token_type: str) -> TokenStruct | None:
    token_parsed: TokenStruct = parse_token(token)
    if not token_parsed:
        return None
    if token_parsed.type != token_type:
        return None

    return token_parsed

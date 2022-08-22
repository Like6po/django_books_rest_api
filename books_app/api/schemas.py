from datetime import datetime

from pydantic import BaseModel


class TokenStruct(BaseModel):
    iss: str = "api_app"
    type: str
    exp: datetime | None = None
    sub: str
    jti: str  # str(uuid.uuid4())
    iat: datetime  # datetime.utnow()

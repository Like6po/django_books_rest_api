from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TokenStruct(BaseModel):
    iss: str = "api_app"
    type: str
    exp: Optional[datetime] = None
    sub: str
    jti: str  # str(uuid.uuid4())
    iat: datetime  # datetime.utnow()

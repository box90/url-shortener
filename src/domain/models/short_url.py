from datetime import datetime

from pydantic import BaseModel


class ShortURL(BaseModel):
    original_url: str
    short_code: str
    created_at: datetime
    expire_at: datetime

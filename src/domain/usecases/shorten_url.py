from datetime import datetime, timedelta
import time

from domain.models.short_url import ShortURL
from domain.repositories.url_repository import URLRepository
from configs import BASE_URL
from utils import generate_code

class ShortenUrlUseCase:
    def __init__(self, repo: URLRepository):
        self.repo = repo

    async def execute(self, original_url: str, expiration: int) -> str:
        now = datetime.utcnow()
        existing = await self.repo.get_by_original(original_url)
        if existing and existing.expire_at > now:
            return BASE_URL + existing.short_code

        short_code = generate_code(original_url + str(time.time()))
        expire_at = now + timedelta(seconds=expiration)

        short_url = ShortURL(
            original_url=original_url,
            short_code=short_code,
            created_at=now,
            expire_at=expire_at
        )
        await self.repo.save(short_url)
        return BASE_URL + short_code
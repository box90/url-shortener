import logging
from datetime import datetime, timedelta
import time

from domain.errors.exceptions import DuplicateKeyCustomException
from domain.models.short_url import ShortURL
from domain.repositories.url_repository import URLRepository
from configs import BASE_URL
from utils import generate_code

logger = logging.getLogger(__name__)

class ShortenUrlUseCase:
    def __init__(self, repo: URLRepository):
        self.repo = repo

    async def execute(self, original_url: str, expiration: int) -> str:
        logger.info(f"Starting URL shortening for: {original_url} with expiration: {expiration} seconds")
        now = datetime.utcnow()
        existing = await self.repo.get_by_original(original_url)
        if existing and existing.expire_at > now:
            logger.info(f"URL already exists and is valid: {existing.short_code}")
            return BASE_URL + existing.short_code

        short_code = generate_code(original_url + str(time.time()))
        expire_at = now + timedelta(seconds=expiration)

        short_url = ShortURL(
            original_url=original_url,
            short_code=short_code,
            created_at=now,
            expire_at=expire_at
        )
        try:
            existing_element = await self.repo.get_by_original(short_url.original_url)
            if existing_element:
                if existing_element.expire_at < now:
                    logger.info(f"URL already exists: {short_url.original_url} and it's expired")
                    return "❌ Shortened URL already exists and it's expired."
                return BASE_URL + short_code

            await self.repo.save(short_url)

        except DuplicateKeyCustomException:
            logger.warning(f"Duplicate short code generated: {short_code}, already exists")
            return "❌ Shortened URL already exists."

        logger.info(f"Shortened URL created: {BASE_URL + short_code}")
        return BASE_URL + short_code
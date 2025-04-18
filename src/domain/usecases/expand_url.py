import logging
from datetime import datetime

from domain.repositories.url_repository import URLRepository

logger = logging.getLogger(__name__)

class ExpandUrlUseCase:
    def __init__(self, repo: URLRepository):
        self.repo = repo

    async def execute(self, short_url: str) -> str:
        logger.info(f"Expanding URL: {short_url}")
        code = short_url.rstrip('/').split('/')[-1]
        obj = await self.repo.get_by_code(code)
        if not obj:
            logger.warning(f"Shortened URL not found: {short_url}")
            return "❌ Shortened URL does not exist."
        if datetime.utcnow() > obj.expire_at:
            logger.warning(f"Shortened URL has expired: {short_url}")
            return "⏰ Shortened URL has expired."
        logger.info(f"Original URL retrieved: {obj.original_url}")
        return obj.original_url
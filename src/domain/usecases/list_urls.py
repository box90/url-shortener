import logging
from configs import BASE_URL
from domain.repositories.url_repository import URLRepository

logger = logging.getLogger(__name__)

class ListUrlsUseCase:
    def __init__(self, repo: URLRepository):
        self.repo = repo

    async def execute(self):
        logger.info("Listing all shortened URLs")
        urls = await self.repo.list_all()
        result = [
            {
                "short_url": BASE_URL + u.short_code,
                "original_url": u.original_url,
                "created_at": u.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "expires_at": u.expire_at.strftime("%Y-%m-%d %H:%M:%S")
            }
            for u in urls
        ]
        logger.info(f"Total URLs listed: {len(result)}")
        return result
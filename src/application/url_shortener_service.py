import logging

from domain.usecases.shorten_url import ShortenUrlUseCase
from domain.usecases.expand_url import ExpandUrlUseCase
from domain.usecases.list_urls import ListUrlsUseCase

logger = logging.getLogger(__name__)

class URLShortenerService:
    def __init__(self, repo):
        self.repo = repo

    async def shorten(self, url: str, expiration: int = None):
        logger.info(f"Service: Shortening URL: {url} with expiration: {expiration}")
        use_case = ShortenUrlUseCase(self.repo)
        result = await use_case.execute(url, expiration)
        if result:
            logger.info(f"Service: Shortened URL result: {result}")
            return result

    async def expand(self, short_url: str):
        logger.info(f"Service: Expanding short URL: {short_url}")
        use_case = ExpandUrlUseCase(self.repo)
        result = await use_case.execute(short_url)
        logger.info(f"Service: Expanded URL result: {result}")
        return result

    async def list_all(self):
        logger.info("Service: Listing all shortened URLs")
        use_case = ListUrlsUseCase(self.repo)
        result = await use_case.execute()
        logger.info(f"Service: Total URLs listed: {len(result)}")
        return result
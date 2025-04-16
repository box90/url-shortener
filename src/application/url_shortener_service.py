from domain.repositories.url_repository import URLRepository

from configs import DEFAULT_EXPIRATION
from domain.usecases.expand_url import ExpandUrlUseCase
from domain.usecases.list_urls import ListUrlsUseCase
from domain.usecases.shorten_url import ShortenUrlUseCase


class URLShortenerService:
    def __init__(self, repository: URLRepository):
        self.repo = repository

    async def shorten(self, original_url: str, expiration: int = DEFAULT_EXPIRATION):
        return await ShortenUrlUseCase(self.repo).execute(original_url, expiration)

    async def expand(self, short_url: str):
        return await ExpandUrlUseCase(self.repo).execute(short_url)

    async def list_all(self):
        return await ListUrlsUseCase(self.repo).execute()

from abc import ABC, abstractmethod
from typing import List

from domain.models.short_url import ShortURL


class URLRepository(ABC):
    @abstractmethod
    async def get_by_original(self, url: str) -> ShortURL | None: pass

    @abstractmethod
    async def get_by_code(self, code: str) -> ShortURL | None: pass

    @abstractmethod
    async def save(self, short_url: ShortURL) -> None: pass

    @abstractmethod
    async def list_all(self) -> List[ShortURL]: pass

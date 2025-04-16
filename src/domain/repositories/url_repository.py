from abc import ABC, abstractmethod
from typing import Optional, List

from domain.models.short_url import ShortURL


class URLRepository(ABC):
    @abstractmethod
    async def get_by_original(self, url: str) -> ShortURL | None: ...

    @abstractmethod
    async def get_by_code(self, code: str) -> ShortURL | None: ...

    @abstractmethod
    async def save(self, short_url: ShortURL) -> None: ...

    @abstractmethod
    async def list_all(self) -> List[ShortURL]: ...

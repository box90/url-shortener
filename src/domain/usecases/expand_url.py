from datetime import datetime

from domain.repositories.url_repository import URLRepository


class ExpandUrlUseCase:
    def __init__(self, repo: URLRepository):
        self.repo = repo

    async def execute(self, short_url: str) -> str:
        code = short_url.rstrip('/').split('/')[-1]
        obj = await self.repo.get_by_code(code)
        if not obj:
            return "❌ Shortened URL does not exist."
        if datetime.utcnow() > obj.expire_at:
            return "⏰ Shortened URL has expired."
        return obj.original_url

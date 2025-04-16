from configs import BASE_URL
from domain.repositories.url_repository import URLRepository


class ListUrlsUseCase:
    def __init__(self, repo: URLRepository):
        self.repo = repo

    async def execute(self):
        urls = await self.repo.list_all()
        return [
            {
                "short_url": BASE_URL + u.short_code,
                "original_url": u.original_url,
                "created_at": u.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "expires_at": u.expire_at.strftime("%Y-%m-%d %H:%M:%S")
            }
            for u in urls
        ]


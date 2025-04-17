from domain.repositories.url_repository import URLRepository


class FakeRepo(URLRepository):
    def __init__(self):
        self.data = {}

    async def get_by_original(self, url):
        return next((v for v in self.data.values() if v.original_url == url), None)

    async def get_by_code(self, code): return self.data.get(code)

    async def save(self, short_url): self.data[short_url.short_code] = short_url

    async def list_all(self): return list(self.data.values())
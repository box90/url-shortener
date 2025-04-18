import pymongo
from pymongo import ASCENDING
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import DuplicateKeyError

from configs import MONGO_URI, DB_NAME, COLLECTION_NAME
from domain.errors.exceptions import DuplicateKeyCustomException
from domain.models.short_url import ShortURL
from domain.repositories.url_repository import URLRepository


class MongoURLRepository(URLRepository):
    def __init__(self):
        self._client = AsyncIOMotorClient(MONGO_URI)
        self._db = self._client[DB_NAME]
        self._collection = self._db[COLLECTION_NAME]
        self._collection.create_index([("expire_at",ASCENDING)], expireAfterSeconds=0)
        self._collection.create_index("original_url", unique=True)

    async def get_by_original(self, url: str):
        doc = await self._collection.find_one({"original_url": url})
        return ShortURL(**doc) if doc else None

    async def get_by_code(self, code: str):
        doc = await self._collection.find_one({"short_code": code})
        return ShortURL(**doc) if doc else None

    async def save(self, short_url: ShortURL):
        try:
            await self._collection.insert_one(short_url.__dict__)
        except DuplicateKeyError:
            raise DuplicateKeyCustomException(f"URL with code {short_url.short_code} already exists.")

    async def list_all(self):
        cursor = self._collection.find({})
        return [ShortURL(**doc) async for doc in cursor]

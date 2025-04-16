from typing import List

from pymongo import MongoClient, ASCENDING
from pymongo.errors import DuplicateKeyError

from configs import MONGO_URI, DB_NAME, COLLECTION_NAME
from domain.models.short_url import ShortURL
from domain.repositories.url_repository import URLRepository
from infrastructure.mongodb.converter import doc_to_model, model_to_doc

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# Create index for uniqueness
collection.create_index("original_url", unique=True)

# Create index for expiration
collection.create_index([("expire_at", ASCENDING)], expireAfterSeconds=0)


class MongoURLRepository(URLRepository):
    async def get_by_original(self, url: str) -> ShortURL | None:
        doc = collection.find_one({"original_url": url})
        if doc:
            return doc_to_model(doc)
        return None

    async def get_by_code(self, code: str) -> ShortURL | None:
        doc = collection.find_one({"short_code": code})
        if doc:
            return doc_to_model(doc)
        return None

    async def save(self, short_url: ShortURL) -> None:
        try:
            doc = model_to_doc(short_url)
            collection.insert_one(doc)
        except DuplicateKeyError:
            raise ValueError(f"Url {short_url.original_url} already exists.")

    async def list_all(self) -> List[ShortURL]:
        docs = collection.find({}, {"_id": 0})
        return [doc_to_model(d) for d in docs]
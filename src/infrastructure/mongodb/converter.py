from domain.models.short_url import ShortURL


def doc_to_model(doc):
    return ShortURL(
        original_url=doc["original_url"],
        short_code=doc["short_code"],
        created_at=doc["created_at"],
        expire_at=doc["expire_at"]
    )

def model_to_doc(short_url: ShortURL):
    return {
        "original_url": short_url.original_url,
        "short_code": short_url.short_code,
        "created_at": short_url.created_at,
        "expire_at": short_url.expire_at
    }
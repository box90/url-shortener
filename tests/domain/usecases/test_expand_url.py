import pytest
from datetime import datetime, timedelta

from domain.models.short_url import ShortURL
from domain.usecases.expand_url import ExpandUrlUseCase
from tests.domain.fake_repo import FakeRepo


@pytest.mark.asyncio
async def test_expand_url_success():
    repo = FakeRepo()
    short_code = "abc123"
    short_url = ShortURL(
        original_url="https://example.com",
        short_code=short_code,
        created_at=datetime.utcnow(),
        expire_at=datetime.utcnow() + timedelta(hours=1)
    )
    await repo.save(short_url)

    use_case = ExpandUrlUseCase(repo)
    result = await use_case.execute(f"http://short.url/{short_code}")

    assert result == "https://example.com"

@pytest.mark.asyncio
async def test_expand_url_not_found():
    repo = FakeRepo()
    use_case = ExpandUrlUseCase(repo)

    result = await use_case.execute("http://short.url/nonexistent")
    assert result == "❌ Shortened URL does not exist."

@pytest.mark.asyncio
async def test_expand_url_expired():
    repo = FakeRepo()
    short_code = "expired123"
    short_url = ShortURL(
        original_url="https://example.com",
        short_code=short_code,
        created_at=datetime.utcnow() - timedelta(days=1),
        expire_at=datetime.utcnow() - timedelta(hours=1)
    )
    await repo.save(short_url)

    use_case = ExpandUrlUseCase(repo)
    result = await use_case.execute(f"http://short.url/{short_code}")

    assert result == "⏰ Shortened URL has expired."
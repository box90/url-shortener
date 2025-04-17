from unittest.mock import AsyncMock
import pytest
from datetime import datetime, timedelta

from domain.models.short_url import ShortURL

@pytest.mark.asyncio
async def test_save_and_get_by_original():
    repo = AsyncMock()
    short = ShortURL(
        original_url="https://example.com",
        short_code="abc123",
        created_at=datetime.utcnow(),
        expire_at=datetime.utcnow() + timedelta(minutes=30)
    )

    await repo.save(short)
    repo.get_by_original.return_value = short

    found = await repo.get_by_original("https://example.com")
    assert found is not None
    assert found.original_url == "https://example.com"

@pytest.mark.asyncio
async def test_save_and_get_expired_url():
    repo = AsyncMock()
    expired_short = ShortURL(
        original_url="https://expired.com",
        short_code="expired123",
        created_at=datetime.utcnow() - timedelta(days=1),
        expire_at=datetime.utcnow() - timedelta(hours=1)
    )

    await repo.save(expired_short)
    repo.get_by_original.return_value = None  # Not found because it's expired

    found = await repo.get_by_original("https://expired.com")
    assert found is None


@pytest.mark.asyncio
async def test_get_nonexistent_url():
    repo = AsyncMock()
    repo.get_by_original.return_value = None  # not existing

    found = await repo.get_by_original("https://nonexistent.com")
    assert found is None


@pytest.mark.asyncio
async def test_update_existing_url():
    repo = AsyncMock()
    short = ShortURL(
        original_url="https://example.com",
        short_code="abc123",
        created_at=datetime.utcnow(),
        expire_at=datetime.utcnow() + timedelta(minutes=30)
    )

    updated_short = ShortURL(
        original_url="https://example.com",
        short_code="abc123",
        created_at=short.created_at,
        expire_at=datetime.utcnow() + timedelta(hours=1)
    )

    await repo.save(short)
    await repo.save(updated_short)
    repo.get_by_original.return_value = updated_short

    found = await repo.get_by_original("https://example.com")
    assert found is not None
    assert found.expire_at > short.expire_at
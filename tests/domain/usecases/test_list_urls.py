import pytest
from datetime import datetime, timedelta

from domain.models.short_url import ShortURL
from domain.usecases.list_urls import ListUrlsUseCase
from tests.domain.fake_repo import FakeRepo


@pytest.mark.asyncio
async def test_list_urls_success():
    repo = FakeRepo()
    now = datetime.utcnow()
    short_url_1 = ShortURL(
        original_url="https://example1.com",
        short_code="code1",
        created_at=now,
        expire_at=now + timedelta(hours=1)
    )
    short_url_2 = ShortURL(
        original_url="https://example2.com",
        short_code="code2",
        created_at=now,
        expire_at=now + timedelta(hours=2)
    )
    await repo.save(short_url_1)
    await repo.save(short_url_2)

    use_case = ListUrlsUseCase(repo)
    result = await use_case.execute()

    assert len(result) == 2
    assert result[0]["short_url"].endswith("code1")
    assert result[1]["short_url"].endswith("code2")
    assert result[0]["original_url"] == "https://example1.com"
    assert result[1]["original_url"] == "https://example2.com"
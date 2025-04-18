import pytest

from configs import BASE_URL
from domain.usecases.shorten_url import ShortenUrlUseCase
from tests.domain.fake_repo import FakeRepo


@pytest.mark.asyncio
async def test_shorten_url_generates_short_code():
    repo = FakeRepo()
    original_url = "https://example.com/some/long/url"
    shortened = await ShortenUrlUseCase(repo).execute(original_url, expiration=3600)

    assert shortened.startswith(BASE_URL)
    assert len(repo.data) == 1

@pytest.mark.asyncio
async def test_shorten_url_returns_existing_short_code_if_not_expired():
    repo = FakeRepo()
    original_url = "https://example.com/some/long/url"
    use_case = ShortenUrlUseCase(repo)

    shortened = await use_case.execute(original_url, expiration=3600)
    existing_shortened = await use_case.execute(original_url, expiration=3600)

    assert shortened == existing_shortened
    assert len(repo.data) == 1


@pytest.mark.asyncio
async def test_shorten_url_does_not_generate_new_code_if_expired():
    repo = FakeRepo()
    original_url = "https://example.com/some/long/url"
    use_case = ShortenUrlUseCase(repo)

    expired_short_url = await use_case.execute(original_url, expiration=-1)  # Expired
    assert expired_short_url.startswith(BASE_URL)

    new_short_url = await use_case.execute(original_url, expiration=3600)
    assert new_short_url == "❌ Shortened URL already exists and it's expired."

    assert len(repo.data) == 1


@pytest.mark.asyncio
async def test_shorten_url_sets_correct_expiration():
    repo = FakeRepo()
    original_url = "https://example.com/some/long/url"
    expiration = 7200
    use_case = ShortenUrlUseCase(repo)

    shortened = await use_case.execute(original_url, expiration=expiration)
    short_code = shortened.replace(BASE_URL, "")
    saved_url = repo.data[short_code]

    assert (saved_url.expire_at - saved_url.created_at).total_seconds() == expiration
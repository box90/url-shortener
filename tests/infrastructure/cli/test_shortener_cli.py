import argparse
import unittest
from unittest.mock import patch

from infrastructure.cli.shortener_cli import run_cli


class TestShortenerCLI(unittest.TestCase):

    @patch("argparse.ArgumentParser.parse_args")
    @patch("application.url_shortener_service.URLShortenerService")
    @patch("infrastructure.mongodb.mongodb_url_repo_impl.MongoURLRepository")
    @patch("builtins.print")
    async def test_minify(self, mock_print, mock_repo, mock_service, mock_args):
        mock_args.return_value = argparse.Namespace(minify="http://example.com", expand=None, list=False)
        mock_service.return_value.shorten.return_value = "http://short.url/abc123"

        await run_cli()

        mock_print.assert_called_once_with("🔗 Shortened URL: http://short.url/abc123")

    @patch("argparse.ArgumentParser.parse_args")
    @patch("application.url_shortener_service.URLShortenerService")
    @patch("infrastructure.mongodb.mongodb_url_repo_impl.MongoURLRepository")
    @patch("builtins.print")
    async def test_expand(self, mock_print, mock_repo, mock_service, mock_args):
        mock_args.return_value = argparse.Namespace(minify=None, expand="http://short.url/abc123", list=False)
        mock_service.return_value.expand.return_value = "http://example.com"

        await run_cli()

        mock_print.assert_called_once_with("🔗 Original URL: http://example.com")

    @patch("argparse.ArgumentParser.parse_args")
    @patch("application.url_shortener_service.URLShortenerService")
    @patch("infrastructure.mongodb.mongodb_url_repo_impl.MongoURLRepository")
    @patch("builtins.print")
    async def test_list(self, mock_print, mock_repo, mock_service, mock_args):
        mock_args.return_value = argparse.Namespace(minify=None, expand=None, list=True)
        mock_service.return_value.list_urls.return_value = [
            {"short_url": "http://short.url/abc123", "original_url": "http://example.com"},
            {"short_url": "http://short.url/xyz789", "original_url": "http://example.org"},
        ]

        await run_cli()

        mock_print.assert_any_call("🔗 Short URL: http://short.url/abc123 -> Original URL: http://example.com")
        mock_print.assert_any_call("🔗 Short URL: http://short.url/xyz789 -> Original URL: http://example.org")
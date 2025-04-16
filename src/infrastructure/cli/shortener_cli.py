import argparse

from application.url_shortener_service import URLShortenerService
from infrastructure.mongodb.mongodb_url_repo_impl import MongoURLRepository


def run_cli():
    parser = argparse.ArgumentParser(description="Hexagonal URL Shortener CLI")
    parser.add_argument("--minify", type=str, help="URL to shorten")
    parser.add_argument("--expand", type=str, help="Short URL to expand")
    parser.add_argument("--list", action="store_true", help="List all shortened URLs")

    args = parser.parse_args()
    service = URLShortenerService(MongoURLRepository())

    if args.minify:
        result = service.shorten(args.minify)
        print(f"🔗 Shortened URL: {result}")
    elif args.expand:
        result = service.expand(args.expand)
        print(f"🌐 Original URL: {result}")
    elif args.list:
        print("📋 All Shortened URLs:")
        for entry in service.list_all():
            print(f"- {entry['short_url']} -> {entry['original_url']} (expires {entry['expires_at']})")
    else:
        print("ℹ️ Use --minify, --expand or --list")

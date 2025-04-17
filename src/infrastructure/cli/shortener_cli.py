import argparse

from application.url_shortener_service import URLShortenerService
from configs import DEFAULT_EXPIRATION
from infrastructure.mongodb.mongodb_url_repo_impl import MongoURLRepository


async def run_cli():
    parser = argparse.ArgumentParser(description="Hexagonal URL Shortener CLI")
    parser.add_argument("--minify", type=str, help="URL to shorten")
    parser.add_argument("--expiration", type=int,
                        help="Expiration time in seconds (default: 3600)", default=DEFAULT_EXPIRATION)
    parser.add_argument("--expand", type=str, help="Short URL to expand")
    parser.add_argument("--list", action="store_true", help="List all shortened URLs")

    args = parser.parse_args()
    service = URLShortenerService(MongoURLRepository())

    if args.minify:
        result = await service.shorten(args.minify, expiration=args.expiration)
        print(f"🔗 Shortened URL: {result}")
    elif args.expand:
        result = await service.expand(args.expand)
        print(f"🌐 Original URL: {result}")
    elif args.list:
        print("📋 All Shortened URLs:")
        for entry in await service.list_all():
            print(f"- {entry['short_url']} -> {entry['original_url']} (expires {entry['expires_at']})")
    else:
        parser.print_help()

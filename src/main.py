import asyncio

from infrastructure.cli.shortener_cli import run_cli

if __name__ == "__main__":
    asyncio.run(run_cli())

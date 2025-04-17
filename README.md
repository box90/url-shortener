# URL Shortener CLI

This project is a **Hexagonal Architecture-based URL Shortener** implemented in Python. It provides a CLI to shorten URLs, expand shortened URLs, and list all stored URLs. The project uses MongoDB as the database and supports optional expiration for shortened URLs.

## Features

- **Shorten URLs**: Generate a shortened URL for a given original URL.
- **Expand URLs**: Retrieve the original URL from a shortened URL.
- **List URLs**: Display all stored URLs with their expiration details.
- **Expiration Support**: Optionally set an expiration time (in seconds) for shortened URLs.

## Prerequisites

- Python 3.8+
- Docker and Docker Compose

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/url-shortener-cli.git
   cd url-shortener-cli
   ```

2. Install dependencies (if running locally):
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### CLI Commands

1. **Shorten a URL**:
   ```bash
   python src/main.py --minify <URL> [--expiration <seconds>]
   ```
   Example:
   ```bash
   python src/main.py --minify https://example.com --expiration 3600
   ```

2. **Expand a shortened URL**:
   ```bash
   python src/main.py --expand <shortened-URL>
   ```
   Example:
   ```bash
   python src/main.py --expand http://short.url/abc123
   ```

3. **List all URLs**:
   ```bash
   python src/main.py --list
   ```

### Using Docker and Docker Compose

1. **Build the Docker image**:
   ```bash
   docker compose build
   ```

2. **Run the CLI commands**:
   - **Shorten a URL**:
     ```bash
     docker compose run --rm app --minify <URL> [--expiration <seconds>]
     ```
     Example:
     ```bash
     docker compose run --rm app --minify https://example.com --expiration 3600
     ```

   - **Expand a shortened URL**:
     ```bash
     docker compose run --rm app --expand <shortened-URL>
     ```
     Example:
     ```bash
     docker compose run --rm app --expand http://short.url/abc123
     ```

   - **List all URLs**:
     ```bash
     docker compose run --rm app --list
     ```

3. **Stop and clean up**:
   ```bash
   docker compose down
   ```

## Project Structure

- `src/`: Contains the source code.
  - `application/`: Application services and use cases.
  - `domain/`: Domain models and interfaces.
  - `infrastructure/`: CLI and database implementations.
- `docker-compose.yml`: Docker Compose configuration.
- `Dockerfile`: Docker image definition.

## Configuration

- MongoDB connection is configured via the `MONGO_URI` environment variable in `docker-compose.yml`.
- Default expiration time is set in the `configs.py` file.

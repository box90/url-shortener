import logging

# MongoDB configurations
MONGO_URI = "mongodb://mongo:27017"
DB_NAME = "url_shortener"
COLLECTION_NAME = "short_urls"

# Configurations for URL shortener service
BASE_URL = "http://myurlshortener.com/"
DEFAULT_EXPIRATION = 3600

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
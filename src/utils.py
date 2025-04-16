import base64
import hashlib


def generate_code(url: str):
    hash_digest = hashlib.sha256(url.encode()).digest()
    base64_encoded = base64.urlsafe_b64encode(hash_digest).decode('utf-8')
    return base64_encoded[:8]
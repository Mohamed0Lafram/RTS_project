import hmac
import hashlib
import os


SECRET_KEY = os.environ.get("BROKER_SECRET", "changeme").encode()


def make_token(node_name: str) -> str:
    """Generate an HMAC-SHA256 token for a node."""
    return hmac.new(SECRET_KEY, node_name.encode(), hashlib.sha256).hexdigest()


def verify_token(node_name: str, token: str) -> bool:
    """Constant-time comparison to prevent timing attacks."""
    expected = make_token(node_name)
    return hmac.compare_digest(expected, token)
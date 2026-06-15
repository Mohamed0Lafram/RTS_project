#!/usr/bin/env python3
"""
authentication.py – HMAC-SHA256 node-authentication helpers.

Each node proves its identity by appending a token = HMAC-SHA256(node_name, secret).
The receiver independently recomputes the HMAC and compares it in constant time
(``hmac.compare_digest``) to prevent timing-side-channel attacks.

Team Secure Swarm – Université Ibn Tofail, Kénitra (2025-2026)
"""

import base64
import hashlib
import hmac as _hmac


def generate_token(node_name: str, secret: str) -> str:
    """
    Generate a HMAC-SHA256 authentication token for *node_name*.

    Parameters
    ----------
    node_name : str
        Canonical name of the ROS2 node (e.g. ``'talker_secure'``).
    secret : str
        Shared secret known by all legitimate participants.

    Returns
    -------
    str
        Base64url-encoded HMAC digest.
    """
    key   = secret.encode('utf-8')
    msg   = node_name.encode('utf-8')
    digest = _hmac.new(key, msg, digestmod=hashlib.sha256).digest()
    return base64.urlsafe_b64encode(digest).decode()


def verify_token(node_name: str, received_token: str, secret: str) -> bool:
    """
    Verify that *received_token* is a valid HMAC for *node_name*.

    Uses ``hmac.compare_digest`` for constant-time comparison.

    Parameters
    ----------
    node_name : str
        Expected node identity.
    received_token : str
        Base64url-encoded token extracted from the incoming message.
    secret : str
        Shared secret.

    Returns
    -------
    bool
        ``True`` if the token is authentic, ``False`` otherwise.
    """
    expected = generate_token(node_name, secret)
    return _hmac.compare_digest(expected, received_token)

#!/usr/bin/env python3
"""
integrity.py – RSA-PSS digital signature helpers.

The publisher signs each (encrypted) message with its RSA-2048 private key.
The subscriber verifies the signature using the matching public key.
Any modification of the ciphertext in transit will cause verification to fail.

Key files are expected at:
  • certificates/private.pem   (kept secret by the publisher)
  • certificates/public.pem    (distributed to all subscribers)

Team Secure Swarm – Université Ibn Tofail, Kénitra (2025-2026)
"""

import base64

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _load_private_key(path: str):
    with open(path, 'rb') as f:
        return serialization.load_pem_private_key(f.read(), password=None)


def _load_public_key(path: str):
    with open(path, 'rb') as f:
        return serialization.load_pem_public_key(f.read())


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def sign_message(message: str, private_key_path: str) -> str:
    """
    Sign *message* with RSA-PSS and return a Base64url-encoded signature.

    Parameters
    ----------
    message : str
        The data to sign (typically the AES-GCM JSON payload).
    private_key_path : str
        Path to the PEM-encoded RSA private key.

    Returns
    -------
    str
        Base64url-encoded signature.
    """
    private_key = _load_private_key(private_key_path)
    sig = private_key.sign(
        message.encode('utf-8'),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH,
        ),
        hashes.SHA256(),
    )
    return base64.urlsafe_b64encode(sig).decode()


def verify_signature(message: str, signature_b64: str, public_key_path: str) -> bool:
    """
    Verify an RSA-PSS *signature* against *message*.

    Parameters
    ----------
    message : str
        The signed data.
    signature_b64 : str
        Base64url-encoded signature as returned by :func:`sign_message`.
    public_key_path : str
        Path to the PEM-encoded RSA public key.

    Returns
    -------
    bool
        ``True`` if the signature is valid, ``False`` otherwise.
    """
    public_key = _load_public_key(public_key_path)
    sig = base64.urlsafe_b64decode(signature_b64)
    try:
        public_key.verify(
            sig,
            message.encode('utf-8'),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH,
            ),
            hashes.SHA256(),
        )
        return True
    except Exception:
        return False

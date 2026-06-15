#!/usr/bin/env python3
"""
encrypt.py – AES-256-GCM encryption / decryption helpers.

AES-GCM provides:
  • Confidentiality  (AES-256 in CTR mode)
  • Authenticity     (GCM authentication tag)
  • High performance (hardware-accelerated on modern CPUs)

Encoding convention:
  The functions return / accept Base64url strings so they travel safely
  inside JSON ROS2 String messages.

Team Secure Swarm – Université Ibn Tofail, Kénitra (2025-2026)
"""

import base64
import json
import os

from cryptography.hazmat.primitives.ciphers.aead import AESGCM


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def encrypt(plaintext: str, key: bytes) -> str:
    """
    Encrypt *plaintext* with AES-256-GCM.

    Parameters
    ----------
    plaintext : str
        The message to protect.
    key : bytes
        32-byte (256-bit) AES key.

    Returns
    -------
    str
        JSON string containing Base64url-encoded ``nonce`` and ``ciphertext``.
    """
    if len(key) != 32:
        raise ValueError(f'AES-256 key must be 32 bytes, got {len(key)}.')

    aesgcm = AESGCM(key)
    nonce  = os.urandom(12)          # 96-bit random nonce (GCM standard)
    ct     = aesgcm.encrypt(nonce, plaintext.encode('utf-8'), None)

    return json.dumps({
        'nonce': base64.urlsafe_b64encode(nonce).decode(),
        'ct':    base64.urlsafe_b64encode(ct).decode(),
    })


def decrypt(payload: str, key: bytes) -> str:
    """
    Decrypt and authenticate an AES-256-GCM payload produced by :func:`encrypt`.

    Parameters
    ----------
    payload : str
        JSON string as returned by :func:`encrypt`.
    key : bytes
        32-byte AES key (must match the one used during encryption).

    Returns
    -------
    str
        Recovered plaintext.

    Raises
    ------
    ValueError
        On authentication failure (tampered ciphertext or wrong key).
    """
    if len(key) != 32:
        raise ValueError(f'AES-256 key must be 32 bytes, got {len(key)}.')

    data  = json.loads(payload)
    nonce = base64.urlsafe_b64decode(data['nonce'])
    ct    = base64.urlsafe_b64decode(data['ct'])

    aesgcm = AESGCM(key)
    try:
        plaintext_bytes = aesgcm.decrypt(nonce, ct, None)
    except Exception as exc:
        raise ValueError(f'AES-GCM decryption / authentication failed: {exc}') from exc

    return plaintext_bytes.decode('utf-8')


import os
import json
import base64
from Cryptodome.Cipher import AES
from Cryptodome.Protocol.KDF import PBKDF2
from Cryptodome.Hash import SHA256, HMAC
from Cryptodome.Random import get_random_bytes


 
SALT_SIZE     = 32      
KEY_SIZE      = 32      
ITERATIONS    = 200_000 
TAG_SIZE      = 16      


# ── Key Derivation ────────────────────────────────────────────────────────────
def derive_key(password: str, salt: bytes) -> bytes:
    """Derive a 256-bit key from a password using PBKDF2-SHA256."""
    return PBKDF2(
        password.encode("utf-8"),
        salt,
        dkLen=KEY_SIZE,
        count=ITERATIONS,
        prf=lambda p, s: HMAC.new(p, s, SHA256).digest()
    )


# ── Encrypt ───────────────────────────────────────────────────────────────────
def encrypt(plaintext: str, password: str) -> str:
    """
    Encrypt plaintext using AES-256-GCM.

    Returns a Base64-encoded JSON blob containing:
      salt, nonce, ciphertext, tag
    """
    salt  = get_random_bytes(SALT_SIZE)
    key   = derive_key(password, salt)
    nonce = get_random_bytes(16)       

    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce, mac_len=TAG_SIZE)
    ciphertext, tag = cipher.encrypt_and_digest(plaintext.encode("utf-8"))

    payload = {
        "salt":       base64.b64encode(salt).decode(),
        "nonce":      base64.b64encode(nonce).decode(),
        "ciphertext": base64.b64encode(ciphertext).decode(),
        "tag":        base64.b64encode(tag).decode(),
    }
    return base64.b64encode(json.dumps(payload).encode()).decode()

    
def decrypt(token: str, password: str) -> str:
    """
    Decrypt a token produced by encrypt().
    Returns "" if the token is invalid, malformed, or decryption fails.
    """
    try:
        payload    = json.loads(base64.b64decode(token).decode())
        salt       = base64.b64decode(payload["salt"])
        nonce      = base64.b64decode(payload["nonce"])
        ciphertext = base64.b64decode(payload["ciphertext"])
        tag        = base64.b64decode(payload["tag"])
    except Exception:
        return ""   # ← malformed token

    key    = derive_key(password, salt)
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce, mac_len=TAG_SIZE)

    try:
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)
    except Exception:
        return ""   # ← wrong password or tampered data

    return plaintext.decode("utf-8")
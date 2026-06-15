#!/usr/bin/env python3
"""
test.py – Self-contained integration tests for the security primitives.
Run directly (no ROS2 required):
  python3 src/secure_connection/secure_connection/test.py

Team Secure Swarm – Université Ibn Tofail, Kénitra (2025-2026)
"""

import os
import sys
import tempfile

# ---------------------------------------------------------------------------
# Make sure we can import siblings regardless of install state
# ---------------------------------------------------------------------------
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from secure_connection.encrypt import encrypt, decrypt
from secure_connection.authentication import generate_token, verify_token
from secure_connection.integrity import sign_message, verify_signature
from secure_connection.generate_key import generate_rsa_keypair

PASS = '\033[92m[PASS]\033[0m'
FAIL = '\033[91m[FAIL]\033[0m'


def test_aes_gcm():
    print('\n--- AES-256-GCM ---')
    key = os.urandom(32)
    plaintext = 'Robot position: x=10, y=5, z=0'

    ciphertext = encrypt(plaintext, key)
    recovered  = decrypt(ciphertext, key)
    assert recovered == plaintext, f'Expected {plaintext!r}, got {recovered!r}'
    print(f'{PASS} encrypt → decrypt roundtrip OK')

    # Wrong key should raise
    wrong_key = os.urandom(32)
    try:
        decrypt(ciphertext, wrong_key)
        print(f'{FAIL} Wrong key should have raised ValueError')
    except ValueError:
        print(f'{PASS} Wrong-key decryption correctly rejected')


def test_hmac_auth():
    print('\n--- HMAC-SHA256 Authentication ---')
    secret = 'super_secret_key'

    token = generate_token('talker_secure', secret)
    assert verify_token('talker_secure', token, secret), 'Valid token rejected'
    print(f'{PASS} Valid token accepted')

    assert not verify_token('talker_secure', 'bad_token', secret), 'Bad token accepted'
    print(f'{PASS} Invalid token rejected')

    assert not verify_token('other_node', token, secret), 'Wrong node accepted'
    print(f'{PASS} Wrong node-name rejected')


def test_rsa_signature():
    print('\n--- RSA-2048-PSS Signature ---')
    with tempfile.TemporaryDirectory() as tmpdir:
        priv_path, pub_path = generate_rsa_keypair(tmpdir)
        message = '{"ct":"abc123","nonce":"xyz"}'

        sig = sign_message(message, priv_path)
        assert verify_signature(message, sig, pub_path), 'Valid sig rejected'
        print(f'{PASS} Valid signature accepted')

        tampered = message + 'X'
        assert not verify_signature(tampered, sig, pub_path), 'Tampered msg accepted'
        print(f'{PASS} Tampered message rejected')


def main():
    print('=' * 50)
    print('  Secure Swarm – Security Primitives Test Suite')
    print('=' * 50)
    try:
        test_aes_gcm()
        test_hmac_auth()
        test_rsa_signature()
        print('\n\033[92mAll tests passed ✔\033[0m\n')
    except AssertionError as exc:
        print(f'\n\033[91mTest FAILED: {exc}\033[0m\n')
        sys.exit(1)


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
listener_secure.py – Secure Subscriber (AES-256-GCM + HMAC + RSA verification).
Team Secure Swarm – Université Ibn Tofail, Kénitra (2025-2026)

Pipeline (inverse of talker_secure):
  receive payload
      → verify token  [HMAC-SHA256  – authentication]
      → verify sign   [RSA-PSS      – integrity]
      → decrypt()     [AES-256-GCM  – confidentiality]
      → log plaintext
"""

import json
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

try:
    from secure_connection.encrypt import decrypt
    from secure_connection.integrity import verify_signature
    from secure_connection.authentication import verify_token
    _CRYPTO_AVAILABLE = True
except ImportError:
    _CRYPTO_AVAILABLE = False


class ListenerSecure(Node):
    def __init__(self):
        super().__init__('listener_secure')

        self.declare_parameter('aes_key_hex', '')
        self.declare_parameter('hmac_secret', 'default_hmac_secret')
        self.declare_parameter('public_key_path',
                               'src/secure_connection/secure_connection/certificates/public.pem')

        self.aes_key_hex  = self.get_parameter('aes_key_hex').value
        self.hmac_secret  = self.get_parameter('hmac_secret').value
        self.pubkey_path  = self.get_parameter('public_key_path').value

        self.subscription = self.create_subscription(
            String, 'robot_topic_secure', self.listener_callback, 10)

        if not _CRYPTO_AVAILABLE:
            self.get_logger().warn(
                'secure_connection package not found – PLAINTEXT fallback mode.')
        self.get_logger().info('ListenerSecure started.')

    # ------------------------------------------------------------------
    def listener_callback(self, msg):
        raw = msg.data

        if not _CRYPTO_AVAILABLE or not self.aes_key_hex:
            self.get_logger().info(f'[PLAIN] {raw}')
            return

        try:
            payload = json.loads(raw)
            ciphertext = payload['ciphertext']
            signature  = payload['signature']
            token      = payload['token']
        except (json.JSONDecodeError, KeyError) as exc:
            self.get_logger().error(f'Malformed payload: {exc}')
            return

        # 1 – Authenticate
        if not verify_token('talker_secure', token, self.hmac_secret):
            self.get_logger().error('AUTHENTICATION FAILED – invalid token!')
            return

        # 2 – Integrity
        if not verify_signature(ciphertext, signature, self.pubkey_path):
            self.get_logger().error('INTEGRITY CHECK FAILED – message tampered!')
            return

        # 3 – Decrypt
        try:
            aes_key   = bytes.fromhex(self.aes_key_hex)
            plaintext = decrypt(ciphertext, aes_key)
            self.get_logger().info(f'[SECURE] {plaintext}')
        except Exception as exc:
            self.get_logger().error(f'DECRYPTION FAILED: {exc}')


def main(args=None):
    rclpy.init(args=args)
    node = ListenerSecure()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

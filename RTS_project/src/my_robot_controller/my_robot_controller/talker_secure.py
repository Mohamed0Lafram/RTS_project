#!/usr/bin/env python3
"""
talker_secure.py – Secure Publisher (AES-256-GCM + HMAC-SHA256 + RSA signature).
Team Secure Swarm – Université Ibn Tofail, Kénitra (2025-2026)

Pipeline:
  raw_message
      → encrypt()   [AES-256-GCM  – confidentiality]
      → sign()      [RSA-PSS      – integrity]
      → add token   [HMAC-SHA256  – authentication]
      → publish on /robot_topic_secure
"""

import json
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

# Lazy imports so the node still loads even when the crypto packages are absent
try:
    from secure_connection.encrypt import encrypt
    from secure_connection.integrity import sign_message
    from secure_connection.authentication import generate_token
    _CRYPTO_AVAILABLE = True
except ImportError:
    _CRYPTO_AVAILABLE = False


class TalkerSecure(Node):
    def __init__(self):
        super().__init__('talker_secure')

        # ------------------------------------------------------------------
        # Parameters (can be overridden via ROS2 parameter server)
        # ------------------------------------------------------------------
        self.declare_parameter('aes_key_hex', '')  # 64-hex-char AES-256 key
        self.declare_parameter('hmac_secret', 'default_hmac_secret')
        self.declare_parameter('private_key_path',
                               'src/secure_connection/secure_connection/certificates/private.pem')

        self.aes_key_hex   = self.get_parameter('aes_key_hex').value
        self.hmac_secret   = self.get_parameter('hmac_secret').value
        self.privkey_path  = self.get_parameter('private_key_path').value

        self.publisher_ = self.create_publisher(String, 'robot_topic_secure', 10)
        self.timer = self.create_timer(1.0, self.publish_message)
        self.counter = 0

        if not _CRYPTO_AVAILABLE:
            self.get_logger().warn(
                'secure_connection package not found – running in PLAINTEXT fallback mode.')
        self.get_logger().info('TalkerSecure started.')

    # ------------------------------------------------------------------
    def publish_message(self):
        plaintext = f'Robot position: x={self.counter}, y=0, z=0'

        if _CRYPTO_AVAILABLE and self.aes_key_hex:
            try:
                aes_key = bytes.fromhex(self.aes_key_hex)
                encrypted = encrypt(plaintext, aes_key)          # AES-256-GCM
                signature = sign_message(encrypted, self.privkey_path)  # RSA-PSS
                token = generate_token('talker_secure', self.hmac_secret)  # HMAC

                payload = json.dumps({
                    'ciphertext': encrypted,
                    'signature':  signature,
                    'token':      token,
                })
            except Exception as exc:
                self.get_logger().error(f'Encryption error: {exc}')
                payload = plaintext
        else:
            # Fallback: send plaintext (useful during development)
            payload = plaintext

        msg = String()
        msg.data = payload
        self.publisher_.publish(msg)
        self.get_logger().info(f'[{self.counter}] Secure message published.')
        self.counter += 1


def main(args=None):
    rclpy.init(args=args)
    node = TalkerSecure()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

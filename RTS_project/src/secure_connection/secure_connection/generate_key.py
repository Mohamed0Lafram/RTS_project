#!/usr/bin/env python3
"""
generate_key.py – Key-management node (Chapter 8).

Responsibilities:
  1. Discover active ROS2 topics.
  2. Generate a unique AES-256 key per topic.
  3. Export the key map to a JSON file for use by talker/listener nodes.
  4. Generate RSA-2048 key pair and write PEM files to certificates/.

Run once before starting the secure nodes:
  ros2 run secure_connection generate_key

Team Secure Swarm – Université Ibn Tofail, Kénitra (2025-2026)
"""

import json
import os
import sys

import rclpy
from rclpy.node import Node

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DEFAULT_CERT_DIR = os.path.join(
    os.path.dirname(__file__), 'certificates')

KEY_MAP_PATH = os.path.join(DEFAULT_CERT_DIR, 'topic_keys.json')


# ---------------------------------------------------------------------------
# RSA helpers
# ---------------------------------------------------------------------------

def generate_rsa_keypair(cert_dir: str = DEFAULT_CERT_DIR):
    """Generate RSA-2048 private / public PEM files."""
    os.makedirs(cert_dir, exist_ok=True)

    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )

    # Write private key
    priv_path = os.path.join(cert_dir, 'private.pem')
    with open(priv_path, 'wb') as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        ))

    # Write public key
    pub_path = os.path.join(cert_dir, 'public.pem')
    with open(pub_path, 'wb') as f:
        f.write(private_key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        ))

    return priv_path, pub_path


# ---------------------------------------------------------------------------
# ROS2 Node
# ---------------------------------------------------------------------------

class GenerateKeyNode(Node):
    """Discover topics and generate per-topic AES-256 keys."""

    def __init__(self):
        super().__init__('generate_key_node')
        self.get_logger().info('GenerateKeyNode started.')

        # Generate RSA key pair
        priv, pub = generate_rsa_keypair()
        self.get_logger().info(f'RSA private key → {priv}')
        self.get_logger().info(f'RSA public  key → {pub}')

        # Discover topics once after a short delay
        self.create_timer(2.0, self._discover_and_generate)

    def _discover_and_generate(self):
        topic_names_and_types = self.get_topic_names_and_types()
        key_map = {}

        for topic_name, _ in topic_names_and_types:
            aes_key = os.urandom(32)                 # 256-bit
            key_map[topic_name] = aes_key.hex()
            self.get_logger().info(
                f'AES key for {topic_name}: {aes_key.hex()[:16]}…')

        os.makedirs(DEFAULT_CERT_DIR, exist_ok=True)
        with open(KEY_MAP_PATH, 'w') as f:
            json.dump(key_map, f, indent=2)

        self.get_logger().info(f'Key map saved → {KEY_MAP_PATH}')
        # Shutdown after one-shot execution
        raise SystemExit(0)


# ---------------------------------------------------------------------------
# Standalone helper (used without ROS2)
# ---------------------------------------------------------------------------

def generate_standalone_keys():
    """Generate RSA key pair and a sample AES key without running a ROS2 node."""
    priv, pub = generate_rsa_keypair()
    aes_key = os.urandom(32)
    print(f'RSA private key : {priv}')
    print(f'RSA public  key : {pub}')
    print(f'AES-256 key     : {aes_key.hex()}')
    return aes_key.hex()


def main(args=None):
    rclpy.init(args=args)
    node = GenerateKeyNode()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

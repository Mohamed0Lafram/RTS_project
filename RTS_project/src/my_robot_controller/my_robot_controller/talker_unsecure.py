#!/usr/bin/env python3
"""
talker_unsecure.py – Publisher without any security layer.
Used as baseline for comparison with the secure version.
Team Secure Swarm – Université Ibn Tofail, Kénitra (2025-2026)
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class TalkerUnsecure(Node):
    def __init__(self):
        super().__init__('talker_unsecure')
        self.publisher_ = self.create_publisher(String, 'robot_topic_unsecure', 10)
        self.timer = self.create_timer(1.0, self.publish_message)
        self.counter = 0
        self.get_logger().info('TalkerUnsecure started (NO security).')

    def publish_message(self):
        msg = String()
        msg.data = f'[UNSECURE] Robot position: x={self.counter}, y=0, z=0'
        self.publisher_.publish(msg)
        self.get_logger().info(f'Published: {msg.data}')
        self.counter += 1


def main(args=None):
    rclpy.init(args=args)
    node = TalkerUnsecure()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

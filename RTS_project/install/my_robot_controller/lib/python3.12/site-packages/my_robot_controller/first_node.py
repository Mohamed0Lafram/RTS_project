#!/usr/bin/env python3
"""
first_node.py - Basic ROS2 node (hello-world).
Team Secure Swarm – Université Ibn Tofail, Kénitra (2025-2026)
"""

import rclpy
from rclpy.node import Node


class FirstNode(Node):
    def __init__(self):
        super().__init__('first_node')
        self.get_logger().info('FirstNode started – hello from Team Secure Swarm!')
        self.timer = self.create_timer(1.0, self.timer_callback)

    def timer_callback(self):
        self.get_logger().info('FirstNode is running …')


def main(args=None):
    rclpy.init(args=args)
    node = FirstNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

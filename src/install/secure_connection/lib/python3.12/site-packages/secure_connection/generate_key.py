import rclpy
from rclpy.node import Node

from Crypto.Random import get_random_bytes
import base64
import subprocess
import os


class FirstNode(Node):

    def __init__(self):
        super().__init__("first_node")

        self.counter_ = 1
        self.create_timer(1.0, self.timer_callback)

        # get topics at startup
        self.topics = self.get_ros2_topics()

        # generate keys for each topic
        self.topic_keys = self.generate_keys_for_topics()

        self.get_logger().info(f"Topics found: {self.topics}")

    # ── get ROS2 topics ─────────────────────────
    def get_ros2_topics(self):
        try:
            result = subprocess.run(
                ["ros2", "topic", "list"],
                capture_output=True,
                text=True,
                check=True
            )

            topics = result.stdout.strip().split("\n")
            return topics

        except subprocess.CalledProcessError as e:
            self.get_logger().error(f"Error getting topics: {e}")
            return []

    # ── generate key ────────────────────────────
    def generate_key(self):
        key_bytes = get_random_bytes(32)  # 256-bit key
        return base64.b64encode(key_bytes).decode()

    # ── assign key per topic ────────────────────
    def generate_keys_for_topics(self):
        keys = {}
        for topic in self.topics:
            keys[topic] = self.generate_key()

            # optional: store in environment
            os.environ[topic] = keys[topic]

        return keys

    # ── timer callback ──────────────────────────
    def timer_callback(self):
        self.get_logger().info(f"Node alive | counter={self.counter_}")
        self.counter_ += 1


# ── main entry point ───────────────────────────
def main():
    rclpy.init()

    node = FirstNode()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
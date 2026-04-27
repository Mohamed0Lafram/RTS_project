import rclpy
from rclpy.node import Node

from Crypto.Random import get_random_bytes
import base64
import subprocess
import os


class FirstNode(Node):

    def __init__(self):
        super().__init__("generate_key")

        # get topics
        self.topics = self.get_ros2_topics()

        # generate keys
        self.topic_keys = self.generate_keys_for_topics()

        self.get_logger().info(f"Topics found: {self.topics}")
        self.get_logger().info("Keys generated successfully")
        self.generate_authorised_talkers()

    # ── get ROS2 topics ─────────────────────────
    def get_ros2_topics(self):
        try:
            result = subprocess.run(
                ["ros2", "topic", "list"],
                capture_output=True,
                text=True,
                check=True
            )

            return result.stdout.strip().split("\n")

        except subprocess.CalledProcessError as e:
            self.get_logger().error(f"Error getting topics: {e}")
            return []

    # ── generate key ────────────────────────────
    def generate_key(self):
        key_bytes = get_random_bytes(32)
        return base64.b64encode(key_bytes).decode()
    
    def generate_authorised_talkers(self):
        key_bytes = get_random_bytes(16)
        os.environ['talker'] = base64.b64encode(key_bytes).decode() 


    def generate_keys_for_topics(self):
        keys = {}

        for topic in self.topics:
            key = self.generate_key()
            keys[topic] = key

            # store in environment with valid variable name
            env_var = topic.replace("/", "_").upper()
            os.environ[env_var] = key

            self.get_logger().info(f"Key generated for {topic} (env: {env_var})")

        return keys



def main():
    rclpy.init()

    node = FirstNode()

    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
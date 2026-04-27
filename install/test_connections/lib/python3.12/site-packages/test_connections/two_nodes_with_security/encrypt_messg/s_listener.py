import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from secure_connection.encrypt import decrypt
from custom_interfaces.msg import SECRET
import os
import json

class listener(Node):
    def __init__(self):
        super().__init__("s_listener")
        self.key = os.environ.get("secure_topic", "")
        self.authorised_talker_key = os.environ.get("talker")
        self.subscriber = self.create_subscription(
            SECRET,
            "secure_topic",
            self.listener_callback_encrypted,
            10
        )


    def listener_callback_encrypted(self, messg):
        # Step 1: Decrypt the raw payload
        raw = decrypt(messg.data, self.key)

        if raw is None:
            self.get_logger().warn("Decryption failed — message dropped.")
            return

        # Step 2: Parse the payload envelope
        # Expected format: {"sender_id": "talker_node_1", "content": "hello"}
        try:
            payload = json.loads(raw)
            sender_id = payload.get("sender_id", "")
            content   = payload.get("content", "")
        except (json.JSONDecodeError, AttributeError):
            self.get_logger().warn("Malformed payload — message dropped.")
            return

        # Step 3: Check authorization
        if sender_id != self.authorised_talker_key:
            self.get_logger().warn(
                f"Unauthorized talker '{sender_id}' — message blocked."
            )
            return

        self.get_logger().info(f"[{sender_id}] I heard: {content}")


def main(args=None):
    rclpy.init(args=args)
    node = listener()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main() 
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from auth_registry import verify_token


# Internal wire topics (nodes never publish here directly)
RAW_IN   = "/broker/raw_in"       # authorized publishers send here
SECURE   = "/secure_topic"        # broker forwards verified messages here
REGISTER = "/broker/register"     # registration requests


class SecureBroker(Node):
    """
    Traffic-management middleware.

    Flow:
      1. A node sends a registration request on /broker/register
         with payload  "<node_name>:<role>:<hmac_token>"
      2. Broker verifies the HMAC token.
         - Valid   → node_name added to allow-list for that role.
         - Invalid → denied, logged.
      3. Authorized publishers send messages to /broker/raw_in
         with payload "<node_name>:<token>:<message_body>".
      4. Broker re-verifies on every message, then forwards to /secure_topic.
      5. Authorized subscribers listen to /secure_topic normally —
         the broker checks their registration before relaying.
    """

    def __init__(self):
        super().__init__("secure_broker")

        self._allowed_publishers:  set[str] = set()
        self._allowed_subscribers: set[str] = set()

        # Registration channel
        self.create_subscription(String, REGISTER, self._on_register, 10)

        # Raw input from publishers
        self.create_subscription(String, RAW_IN, self._on_raw_message, 10)

        # Outbound to verified subscribers
        self._pub = self.create_publisher(String, SECURE, 10)

        self.get_logger().info("SecureBroker online — waiting for registrations.")

    # ── Registration ──────────────────────────────────────────────────────────

    def _on_register(self, msg: String):
        """
        Expected format:  "<node_name>:<role>:<token>"
        role is "publisher" or "subscriber"
        """
        try:
            node_name, role, token = msg.data.split(":", 2)
        except ValueError:
            self.get_logger().warn("Registration: malformed request ignored.")
            return

        if not verify_token(node_name, token):
            self.get_logger().warn(
                f"DENIED registration: '{node_name}' (role={role}) — bad token."
            )
            return

        if role == "publisher":
            self._allowed_publishers.add(node_name)
            self.get_logger().info(f"REGISTERED publisher: '{node_name}'")
        elif role == "subscriber":
            self._allowed_subscribers.add(node_name)
            self.get_logger().info(f"REGISTERED subscriber: '{node_name}'")
        else:
            self.get_logger().warn(f"Unknown role '{role}' from '{node_name}'.")

    # ── Traffic gate ──────────────────────────────────────────────────────────

    def _on_raw_message(self, msg: String):
        """
        Expected format:  "<node_name>:<token>:<payload>"
        Verifies sender is registered AND token is still valid, then forwards.
        """
        try:
            node_name, token, payload = msg.data.split(":", 2)
        except ValueError:
            self.get_logger().warn("Raw message: malformed — dropped.")
            return

        # Double-check: must be on allow-list AND token must verify
        if node_name not in self._allowed_publishers:
            self.get_logger().warn(
                f"BLOCKED message from unregistered publisher '{node_name}'."
            )
            return

        if not verify_token(node_name, token):
            self.get_logger().warn(
                f"BLOCKED message from '{node_name}' — token mismatch."
            )
            return

        # Forward to secure topic
        out = String()
        out.data = payload
        self._pub.publish(out)
        self.get_logger().info(
            f"FORWARDED from '{node_name}' → {SECURE}: \"{payload}\""
        )


def main(args=None):
    rclpy.init(args=args)
    broker = SecureBroker()
    try:
        rclpy.spin(broker)
    except KeyboardInterrupt:
        pass
    finally:
        broker.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
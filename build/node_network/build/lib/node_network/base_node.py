import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import random
import os

try:
    from secure_connection.encrypt import encrypt, decrypt
except ImportError:
    # Fallback if secure_connection not available
    def encrypt(plaintext: str, password: str) -> str:
        return plaintext
    
    def decrypt(ciphertext: str, password: str) -> str:
        return ciphertext


COLOURS = {
    "Alpha": "\033[94m",
    "Beta":  "\033[92m",
    "Gamma": "\033[93m",
    "Delta": "\033[91m",
    "RESET": "\033[0m",
}


def log(name, msg):
    c = COLOURS.get(name, "")
    r = COLOURS["RESET"]
    print(f"{c}[{name}]{r} {msg}", flush=True)


def get_key(topic: str) -> str:
    """Get encryption key for a topic from environment variables."""
    # Convert topic name to environment variable name
    env_key = topic.replace("/", "_").upper()
    return os.environ.get(env_key, "")


class BaseNode(Node):

    RING = ["Alpha", "Beta", "Gamma", "Delta"]

    def __init__(self, name: str):
        super().__init__(name.lower() + "_node")

        self.name = name

        idx = self.RING.index(name)
        upstream = self.RING[(idx - 1) % len(self.RING)]

        self.my_topic = f"/{name.lower()}/status"
        self.upstream_topic = f"/{upstream.lower()}/status"

        # 🔑 keys from env
        self.my_key = get_key(self.my_topic)
        self.upstream_key = get_key(self.upstream_topic)

        self.pub = self.create_publisher(String, self.my_topic, 10)

        self.create_subscription(
            String,
            self.upstream_topic,
            self.on_message,
            10
        )

        period = 2.0 + random.uniform(0, 1)
        self.create_timer(period, self.send_message)

        log(name, f"online | encrypted ring node")

    # ── receive (decrypt) ─────────────────────
    def on_message(self, msg: String):
        try:
            plain = decrypt(msg.data, self.upstream_key)
            log(self.name, f"← decrypted: {plain}")
        except Exception:
            log(self.name, "❌ decryption failed")

    # ── send (encrypt) ────────────────────────
    def send_message(self):
        msg = String()

        plaintext = f"[{self.name}] hello"
        msg.data = encrypt(plaintext, self.my_key)

        self.pub.publish(msg)
        log(self.name, f"→ encrypted sent")
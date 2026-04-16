import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import threading
import time
import random
import sys


# ── Shared colour codes for pretty terminal output ────────────────────────────
COLOURS = {
    "Alpha": "\033[94m",   # blue
    "Beta":  "\033[92m",   # green
    "Gamma": "\033[93m",   # yellow
    "Delta": "\033[91m",   # red
    "RESET": "\033[0m",
}

def log(name: str, msg: str):
    c = COLOURS.get(name, "")
    r = COLOURS["RESET"]
    print(f"{c}[{name}]{r} {msg}", flush=True)


#Base node
class BaseNode(Node):
    """
    Each node:
      • publishes on  /<name>/status        (peer-to-peer channel)
      • subscribes to /<upstream>/status    (listens to one neighbour)
      • publishes on  /mesh/broadcast       (global channel)
      • subscribes to /mesh/broadcast       (hears every broadcast)
    """

    RING = ["Alpha", "Beta", "Gamma", "Delta"]   # clockwise ring

    def __init__(self, name: str):
        super().__init__(name.lower() + "_node")
        self.name = name
        idx            = self.RING.index(name)
        upstream_name  = self.RING[(idx - 1) % len(self.RING)]

        # ── publishers 
        self.pub_status    = self.create_publisher(
            String, f"/{name.lower()}/status", 10)
        self.pub_broadcast = self.create_publisher(
            String, "/mesh/broadcast", 10)

        # ── subscriptions
        self.create_subscription(
            String,
            f"/{upstream_name.lower()}/status",
            self._on_peer_msg,
            10,
        )
        self.create_subscription(
            String,
            "/mesh/broadcast",
            self._on_broadcast,
            10,
        )

        # ── periodic publish timer 
        period = 2.0 + random.uniform(0, 0.5)   # slight jitter per node
        self.create_timer(period, self._publish_status)

        log(name, f"online — listening to {upstream_name} on ring")

    # ── callbacks 
    def _on_peer_msg(self, msg: String):
        log(self.name, f"← peer msg  : {msg.data}")

    def _on_broadcast(self, msg: String):
        # Ignore our own broadcasts to keep the log readable
        if msg.data.startswith(f"[{self.name}]"):
            return
        log(self.name, f"← broadcast : {msg.data}")

    # ── periodic publisher 
    def _publish_status(self):
        now    = self.get_clock().now().to_msg()
        status = f"[{self.name}] tick @ {now.sec}.{now.nanosec // 1_000_000:03d}s"

        self.pub_status.publish(String(data=status))
        self.pub_broadcast.publish(String(data=status))
        log(self.name, f"→ published : {status}")


    


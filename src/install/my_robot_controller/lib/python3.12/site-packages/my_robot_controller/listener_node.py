

import rclpy
from rclpy.node import Node
from std_msgs.msg import String



class listener_node(Node):

    def __init__(self):
        super().__init__("listener")

        self.subscriber = self.create_subscription(String,"chatter",self.listener_callback,10)

    def listener_callback(self,messg):
        self.get_logger().info(f"I heard this message : {messg.data}")

def main(args=None):

    rclpy.init(args=args)

    node = listener_node()
    rclpy.spin(node)
    
    rclpy.shutdown()


if __name__ == "__main__":
    main()

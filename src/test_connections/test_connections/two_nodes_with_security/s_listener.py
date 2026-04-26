

import rclpy
from rclpy.node import Node
from std_msgs.msg import String,Header
from secure_connection.encrypt import  decrypt
import os 



class listener(Node):

    def __init__(self):
        super().__init__("s_listener")
        self.key = os.environ.get("secure_topic", "")

        self.subscriber = self.create_subscription(String,"secure_topic",self.listener_callback_encrypted,10)

    def listener_callback_encrypted(self,messg):
        content = decrypt(messg.data, self.key)
        self.get_logger().info(f"I heard this message : {content} ")

def main(args=None):

    rclpy.init(args=args)

    node = listener()
    rclpy.spin(node)
    
    rclpy.shutdown()


if __name__ == "__main__":
    main()

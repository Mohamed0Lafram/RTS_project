

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from test_latency.msg import Message
from secure_connection.encrypt import encrypt, decrypt
import os 




class listener(Node):

    def __init__(self,type):
        super().__init__("listener")
        self.key = os.environ.get("chatter", "")
        if type == "normal":
            self.subscriber = self.create_subscription(Message,"chatter",self.listener_callback,10)
        else : 
            self.subscriber = self.create_subscription(Message,"chatter",self.listener_callback_encrypted,10)

    def listener_callback(self,messg):
        latency = messg.time - self.get_clock().now().nanoseconds / 1e9
        self.get_logger().info(f"I heard this message : {messg.content} with a latency : {latency}")

    def listener_callback_encrypted(self,messg):
        latency = decrypt(messg.content, self.key)
        self.get_logger().info(f"I heard this message : {messg.content} with a latency : {latency}")

def main(args=None):

    rclpy.init(args=args)

    type = input("enter the connection type : ")
    node = listener(type)
    rclpy.spin(node)
    
    rclpy.shutdown()


if __name__ == "__main__":
    main()

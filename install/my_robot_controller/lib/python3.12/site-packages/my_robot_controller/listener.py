

import rclpy
from rclpy.node import Node
from std_msgs.msg import String,Header
from secure_connection.encrypt import encrypt, decrypt
import os 
from builtin_interfaces.msg import Time



class listener(Node):

    def __init__(self,type):
        super().__init__("listener")
        self.key = os.environ.get("chatter", "")
        if type == "normal":
            self.subscriber = self.create_subscription(Header,"chatter",self.listener_callback,10)
        else : 
            self.subscriber = self.create_subscription(Header,"chatter",self.listener_callback_encrypted,10)

    def listener_callback(self,messg):
        now = self.get_clock().now()
        sent_time = messg.stamp
        latency = (now - sent_time).nanoseconds / 1e6
        self.get_logger().info(f"I heard this message : {messg.frame_id} with a latency : {latency}")

    def listener_callback_encrypted(self,messg):
        now = self.get_clock().now()
        sent_time = rclpy.time.Time.from_msg(messg.stamp)
        latency = (now - sent_time).nanoseconds / 1e6
        content = decrypt(messg.frame_id, self.key)
        self.get_logger().info(f"I heard this message : {content} with a latency : {latency}")

def main(args=None):

    rclpy.init(args=args)

    type = input("enter the connection type : ")
    node = listener(type)
    rclpy.spin(node)
    
    rclpy.shutdown()


if __name__ == "__main__":
    main()



import rclpy
from rclpy.node import Node
from std_msgs.msg import String,Header
from builtin_interfaces.msg import Time
from secure_connection.encrypt import encrypt, decrypt
import os 


class talker(Node):

    def __init__(self,type):
        super().__init__("talker")

        self.publisher = self.create_publisher(Header,'chatter',10)
        self.key = os.environ.get("chatter", "")

        if type == "normal":
            self.create_timer(1.0,self.publish_message)
        else : 
            self.create_timer(1.0,self.publish_message_encrypted)
    
    def publish_message(self): #no encryption
        messg = Header()
        messg.frame_id = "wewe"
        now = self.get_clock().now()
        messg.stamp = Time(sec=now.seconds_nanoseconds()[0], nanosec=now.seconds_nanoseconds()[1])

        self.publisher.publish(messg)

        self.get_logger().info(f"i have published {messg.frame_id} at {messg.stamp.sec}.{messg.stamp.nanosec}")
    
    def publish_message_encrypted(self):
        messg = Header()
        messg.frame_id = encrypt("wewe", self.key)
        now = self.get_clock().now()
        messg.stamp = Time(sec=now.seconds_nanoseconds()[0], nanosec=now.seconds_nanoseconds()[1])


        self.publisher.publish(messg)
        self.get_logger().info(f"i have published encrypted message at {messg.stamp.sec}.{messg.stamp.nanosec}")

def main(args=None):

    rclpy.init(args=args)

    node = talker("encrypt")
    rclpy.spin(node)

    rclpy.shutdown()


if __name__ == "__main__":
    main()

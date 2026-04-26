

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from test_latency.msg import Message
from secure_connection.encrypt import encrypt, decrypt
import os 


class talker(Node):

    def __init__(self,type):
        super().__init__("talker")

        self.publisher = self.create_publisher(Message,'chatter',10)
        self.key = os.environ.get("chatter", "")

        if type == "normal":
            self.create_timer(5.0,self.publish_message)
        else : 
            self.create_timer(5.0,self.publish_message)
    
    def publish_message(self): #no encryption
        messg = Message()
        messg.content = "wewe"
        messg.time = self.get_clock().now().nanoseconds / 1e9

        self.publisher.publish(messg)

        self.get_logger().info(f"i have published {messg.content} at {messg.time}")
    
    def publish_message_encrypted(self):
        messg = Message()
        messg.content = encrypt("wewe", self.key)
        messg.time = self.get_clock().now().nanoseconds / 1e9


        self.pub.publish(messg)
        self.get_logger().info(f"i have published {messg.content} at {messg.time}")

def main(args=None):

    rclpy.init(args=args)

    node = talker()
    rclpy.spin(node)

    rclpy.shutdown()


if __name__ == "__main__":
    main()

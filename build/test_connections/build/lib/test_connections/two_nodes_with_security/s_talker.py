import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from secure_connection.encrypt import encrypt
import os 


class talker(Node):

    def __init__(self):
        super().__init__("s_talker")

        self.publisher = self.create_publisher(String,'secure_topic',10)
        self.key = os.environ.get("secure_topic", "")


        self.create_timer(1.0,self.publish_message_encrypted)

    def publish_message_encrypted(self):
        messg = String()
        messg.data = encrypt("wewe", self.key)

        self.publisher.publish(messg)
        self.get_logger().info(f"i have published encrypted message ")

def main(args=None):

    rclpy.init(args=args)

    node = talker()
    rclpy.spin(node)

    rclpy.shutdown()


if __name__ == "__main__":
    main()

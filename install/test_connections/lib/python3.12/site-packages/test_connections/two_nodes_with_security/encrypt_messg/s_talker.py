import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from secure_connection.encrypt import encrypt
from custom_interfaces.msg import SECRET
import os 
import json

class talker(Node):

    def __init__(self):
        super().__init__("s_talker")

        self.publisher = self.create_publisher(SECRET,'secure_topic',10)
        self.key = os.environ.get("secure_topic", "")
        self.talker_key = os.environ.get("talker")

        self.create_timer(1.0,self.publish_message_encrypted)
#{"sender_id": "talker_node_1", "content": "hello"}
    def publish_message_encrypted(self):
        messg = SECRET()
        data = {
            "sender_id":self.talker_key,
            "content":"wewe"
        }
        data = json.dumps(data)
        messg.data = encrypt(str(data), self.key)
        messg.id = "connection 1"

        self.publisher.publish(messg)
        self.get_logger().info(f"i have published encrypted message ")

def main(args=None):

    rclpy.init(args=args)

    node = talker()
    rclpy.spin(node)

    rclpy.shutdown()


if __name__ == "__main__":
    main()

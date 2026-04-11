

import rclpy
from rclpy.node import Node
from std_msgs.msg import String



class talker_node(Node):

    def __init__(self):
        super().__init__("talker")

        self.publisher = self.create_publisher(String,'chatter',10)

        self.create_timer(1.0,self.publish_message)
    
    def publish_message(self):
        messg = String()
        messg.data = "wewe"

        self.publisher.publish(messg)

        self.get_logger().info(f"i have published {messg.data}")

def main(args=None):

    rclpy.init(args=args)

    node = talker_node()
    rclpy.spin(node)

    rclpy.shutdown()


if __name__ == "__main__":
    main()

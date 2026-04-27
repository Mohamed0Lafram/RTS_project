import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from custom_interfaces.msg import SECRET

class ghost_talker(Node):
    def __init__(self):
        super().__init__('ghost_talker')
        self.publisher_ = self.create_publisher(SECRET, '/secure_topic', 10)
        self.timer = self.create_timer(1.0, self.timer_callback)
        self.count = 0

    def timer_callback(self):
        msg = SECRET()
        msg.data = f'iam unautorised talker'
        msg.id = "44"
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing: "{msg.data}"')
        self.count += 1


def main(args=None):
    rclpy.init(args=args)
    node = ghost_talker()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from custom_interfaces.msg import SECRET

class ghost_listener(Node):
    def __init__(self):
        super().__init__('ghost_listener')
        self.subscription = self.create_subscription(
            SECRET,
            '/secure_topic',
            self.listener_callback,
            10,    
        )

    def listener_callback(self, msg: String):
        self.get_logger().info(f'Heard: "{msg.data}"')


def main(args=None):
    rclpy.init(args=args)
    node = ghost_listener()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
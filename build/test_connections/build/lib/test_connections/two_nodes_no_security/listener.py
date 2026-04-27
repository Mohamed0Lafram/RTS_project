import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from custom_interfaces.msg import SECRET

class ListenerNode(Node):
    def __init__(self):
        super().__init__('listener')
        self.subscription = self.create_subscription(
            SECRET,
            '/chatter',
            self.listener_callback,
            10,          # QoS queue depth
        )

    def listener_callback(self, msg: String):
        self.get_logger().info(f'Heard: {msg}  id : {msg.id}')


def main(args=None):
    rclpy.init(args=args)
    node = ListenerNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
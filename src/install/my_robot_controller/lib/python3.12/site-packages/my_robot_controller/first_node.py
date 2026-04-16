


import rclpy
from rclpy.node import Node




class first_node(Node):

    def __init__(self):
        super().__init__("first_node")
        self.counter_ = 1
        self.create_timer(1.0,self.timer_callback)
    
    def timer_callback(self):
        self.get_logger().info(f'hello form node 1 at {str(self.counter_)}')
        self.counter_ += 1


def main(args = None):
    rclpy.init(args=args)

    node = first_node()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()
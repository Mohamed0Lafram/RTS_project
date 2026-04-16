import rclpy
from .base_node import BaseNode




def main():
    rclpy.init()
    node = BaseNode("Gamma")

    rclpy.spin(node)
    node.destroy_node()

if __name__ == "__main__":
    main()
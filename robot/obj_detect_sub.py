import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32 
import cv2.aruco as aruco
import numpy as np

class ArucoSubscriber(Node):
    def __init__(self):
        super().__init__('check_sub')
        self.subscription = self.create_subscription(
            Int32 ,
            'check_seal',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        check_num = [msg.data]
        print(check_num)
        self.get_logger().info(f'Received: {check_num}')
        #self.get_logger().info(f'Received: {msg.data}')

def main(args=None):
    rclpy.init()
    node = ArucoSubscriber()
    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
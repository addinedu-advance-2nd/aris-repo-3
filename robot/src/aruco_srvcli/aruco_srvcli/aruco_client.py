import rclpy
from rclpy.node import Node
from msg_srv_def.srv import GetArucoIds
import time

class ArucoClient(Node):
    def __init__(self):
        super().__init__('aruco_client_node')
        self.client = self.create_client(GetArucoIds, 'get_aruco_ids')

        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('서비스를 기다리는 중...')
        self.req = GetArucoIds.Request()

    def send_request(self):
        request = GetArucoIds.Request()
        self.get_logger().info('Aruco ID 요청 중...')
        future = self.client.call_async(request)

        # 응답을 기다립니다.
        rclpy.spin_until_future_complete(self, future)

        # 요청이 완료되었는지 확인
        if future.done():
            if future.result() is not None:
                self.get_logger().info(f'감지된 ArUco ID 상태: {future.result().ids}')
            else:
                self.get_logger().error('서비스 호출 실패')
        else:
            self.get_logger().error('서비스 호출이 완료되지 않음')

def main(args=None):
    rclpy.init()
    client = ArucoClient()

    try:
        while rclpy.ok():
            time.sleep(1)
            client.send_request()
  # 요청 후 2초 대기
    except KeyboardInterrupt:
        pass
    finally:
        rclpy.shutdown()

if __name__ == '__main__':
    main()

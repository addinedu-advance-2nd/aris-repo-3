from msg_srv_def.srv import GetArucoIds
import rclpy
from rclpy.node import Node
import cv2
import cv2.aruco as aruco
import threading

class VideoThread(threading.Thread):
    def __init__(self, camera_name, camera_index, node):
        super().__init__()
        self.camera_name = camera_name
        self.camera_index = camera_index
        self.node = node
        self.capture = cv2.VideoCapture(camera_index)

        if not self.capture.isOpened():
            self.node.get_logger().error(f"카메라 {camera_index}를 열 수 없습니다.")
            raise Exception(f"카메라 {camera_index}를 열 수 없습니다.")

        self.marker_ids = []
        #self.place = [False, False]  # [ID 0, ID 1, ID 2]
        self.running = True

    def run(self):
        self.node.get_logger().info("서버가 실행되고 있습니다. 비디오 스트림을 시작합니다.")
        while self.running:
            ret, frame = self.capture.read()
            if ret:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                corners, ids, _ = aruco.detectMarkers(gray, aruco.getPredefinedDictionary(aruco.DICT_6X6_250))

                # ID 상태 초기화
                self.place = [False, False, False]

                if ids is not None:
                    self.marker_ids = [int(id[0]) for id in ids]
                    aruco.drawDetectedMarkers(frame, corners)

                    # ID 0, 1, 2의 감지 상태 업데이트
                    for marker_id in self.marker_ids:
                        if marker_id < 3:  # 0, 1, 2에 대해서만 업데이트
                            self.place[marker_id] = True

                    self.node.get_logger().info(f"{self.camera_name}: ArUco 마커 ID: {self.marker_ids}")
                    self.node.get_logger().info(f"{self.place}")
                else:
                    self.node.get_logger().info("감지된 ArUco 마커가 없습니다.")
                    self.node.get_logger().info(f"{self.place}")

                cv2.imshow(self.camera_name, frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    self.stop()
                    break

    def stop(self):
        self.running = False
        self.capture.release()
        cv2.destroyAllWindows()

    def get_marker_status(self):
        return self.place

class ArucoServiceNode(Node):
    def __init__(self):
        super().__init__('aruco_service_node')
        self.video_thread = VideoThread('Camera', 2, self)
        self.video_thread.start()
        self.service = self.create_service(GetArucoIds, 'get_aruco_ids', self.get_aruco_ids)

    def get_aruco_ids(self, request, response):
        response.ids = self.video_thread.get_marker_status()
        if not any(response.ids):
            self.get_logger().info("현재 감지된 ArUco ID가 없습니다.")
        else:
            self.get_logger().info(f"전송할 ArUco ID: {response.ids}")
        return response

def main(args=None):
    rclpy.init()
    node = ArucoServiceNode()
    
    try:
        rclpy.spin(node)
    finally:
        node.video_thread.stop()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

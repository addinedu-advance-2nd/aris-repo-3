import numpy as np
import rclpy
from rclpy.node import Node
import cv2
from ultralytics import YOLO
from std_msgs.msg import Int32  # 수정: Int32를 직접 가져옵니다.
import time

class IceCreamSealNode(Node):
    def __init__(self):
        super().__init__('icecreamseal')
        self.publisher = self.create_publisher(Int32, 'check_seal', 10)
        self.model = YOLO('/home/d/runs/detect/train/weights/best.pt')  # 모델 로드
        self.cap = cv2.VideoCapture(2)  # 웹캠 열기
        self.last_publish_time = time.time()

        self.run()

    def run(self):
        while rclpy.ok():
            ret, frame = self.cap.read()
            if not ret:
                self.get_logger().error("웹캠을 열 수 없습니다.")
                break

            # 가우시안 블러 적용
            blur_frame = cv2.GaussianBlur(frame, (3, 3), 4)

            # 모델을 사용하여 객체 탐지
            detect_params = self.model.predict(source=[blur_frame], conf=0.70, save=False, verbose=False)

            # 첫 번째 이미지에 대한 결과 가져오기
            DP = detect_params[0]

            # 결과를 프레임에 표시
            annotated_frame = DP.plot()  # 결과를 프레임에 그리기

            # 객체 탐지 여부 확인
            obj_detected = 1 if len(DP.boxes) > 0 else 0
            self.get_logger().info(f"Object Detected: {obj_detected}")

            # 1초마다 퍼블리시
            current_time = time.time()
            if current_time - self.last_publish_time >= 1.0:
                msg = Int32()
                msg.data = obj_detected
                self.publisher.publish(msg)  # 퍼블리셔 사용
                self.last_publish_time = current_time

            # 결과 프레임을 화면에 표시
            cv2.imshow('YOLOv8 Ice Cream Detection', annotated_frame)

            # 'q' 키를 눌러 종료
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # 자원 해제
        self.cap.release()
        cv2.destroyAllWindows()

def main():
    rclpy.init()
    node = IceCreamSealNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.cap.release()
        cv2.destroyAllWindows()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

"""
File test chức năng nhận diện tư thế ngồi thẳng trước camera
Sử dụng MediaPipe Pose để nhận diện tư thế
"""

import cv2
import mediapipe as mp
import time

class PoseDetector:
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.mp_drawing = mp.solutions.drawing_utils
        
    def detect_sitting_straight(self, landmarks):
        """
        Kiểm tra xem người có đang ngồi thẳng không
        Dựa vào góc giữa các điểm: vai, khuỷu tay, cổ tay
        """
        if not landmarks:
            return False
        
        try:
            # Lấy các điểm quan trọng
            left_shoulder = landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_SHOULDER]
            right_shoulder = landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_SHOULDER]
            left_elbow = landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_ELBOW]
            right_elbow = landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_ELBOW]
            left_wrist = landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_WRIST]
            right_wrist = landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_WRIST]
            nose = landmarks.landmark[self.mp_pose.PoseLandmark.NOSE]
            
            # Kiểm tra visibility (độ tin cậy)
            if (left_shoulder.visibility < 0.5 or right_shoulder.visibility < 0.5 or
                nose.visibility < 0.5):
                return False
            
            # Tính toán góc giữa vai và mũi (để kiểm tra ngồi thẳng)
            # Nếu mũi ở giữa hai vai và không quá thấp/quá cao -> ngồi thẳng
            shoulder_mid_y = (left_shoulder.y + right_shoulder.y) / 2
            shoulder_mid_x = (left_shoulder.x + right_shoulder.x) / 2
            
            # Kiểm tra mũi có ở giữa hai vai không (theo chiều ngang)
            nose_x_diff = abs(nose.x - shoulder_mid_x)
            
            # Kiểm tra mũi có ở vị trí hợp lý so với vai (không quá thấp, không quá cao)
            nose_y_diff = nose.y - shoulder_mid_y
            
            # Điều kiện ngồi thẳng:
            # 1. Mũi ở giữa hai vai (sai lệch ngang < 0.15)
            # 2. Mũi ở trên vai một khoảng hợp lý (0.05 < diff < 0.25)
            # 3. Hai vai gần như ngang nhau (chênh lệch < 0.1)
            shoulder_level_diff = abs(left_shoulder.y - right_shoulder.y)
            
            is_straight = (
                nose_x_diff < 0.15 and  # Mũi ở giữa vai
                0.05 < nose_y_diff < 0.25 and  # Mũi ở vị trí hợp lý so với vai
                shoulder_level_diff < 0.1  # Hai vai ngang nhau
            )
            
            return is_straight
            
        except Exception as e:
            print(f"Lỗi khi kiểm tra tư thế: {e}")
            return False

def list_available_cameras():
    """Liệt kê các camera có sẵn"""
    available_cameras = []
    print("Đang kiểm tra các camera có sẵn...")
    
    # Thử mở các camera từ 0 đến 9
    for i in range(10):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            ret, _ = cap.read()
            if ret:
                available_cameras.append(i)
                print(f"  ✓ Camera {i}: Có sẵn")
            cap.release()
        else:
            break
    
    return available_cameras

def select_camera():
    """Cho phép người dùng chọn camera"""
    cameras = list_available_cameras()
    
    if not cameras:
        print("Không tìm thấy camera nào!")
        return None
    
    if len(cameras) == 1:
        print(f"\nChỉ có 1 camera, sử dụng Camera {cameras[0]}")
        return cameras[0]
    
    print(f"\nTìm thấy {len(cameras)} camera:")
    for i, cam_id in enumerate(cameras):
        print(f"  [{i+1}] Camera {cam_id}")
    
    while True:
        try:
            choice = input(f"\nChọn camera (1-{len(cameras)}) hoặc Enter để dùng Camera {cameras[0]}: ").strip()
            if not choice:
                return cameras[0]
            
            idx = int(choice) - 1
            if 0 <= idx < len(cameras):
                return cameras[idx]
            else:
                print(f"Vui lòng chọn số từ 1 đến {len(cameras)}")
        except ValueError:
            print("Vui lòng nhập số hợp lệ!")
        except KeyboardInterrupt:
            return None

def test_pose_detection():
    """Test chức năng nhận diện tư thế"""
    print("=" * 50)
    print("TEST NHẬN DIỆN TƯ THẾ NGỒI THẲNG")
    print("=" * 50)
    
    # Chọn camera
    camera_id = select_camera()
    if camera_id is None:
        print("Đã hủy.")
        return
    
    print(f"\nĐang khởi động Camera {camera_id}...")
    print("\nHướng dẫn:")
    print("- Ngồi thẳng trước camera")
    print("- Giữ tư thế trong 3 giây để tắt báo thức")
    print("- Nhấn 'q' để thoát")
    print("- Nhấn 'r' để reset đếm")
    print("- Nhấn 'c' để chuyển đổi camera")
    print("- Nhấn phím số (0-9) để chuyển sang camera tương ứng")
    print()
    
    detector = PoseDetector()
    cap = cv2.VideoCapture(camera_id)
    
    if not cap.isOpened():
        print(f"Lỗi: Không thể mở Camera {camera_id}!")
        return
    
    # Thiết lập độ phân giải
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    # Biến đếm
    straight_count = 0
    required_time = 3.0  # Cần giữ tư thế trong 3 giây
    start_time = None
    last_reset_time = time.time()
    frame_error_count = 0
    max_frame_errors = 10  # Cho phép tối đa 10 lần lỗi liên tiếp
    
    print("Camera đã sẵn sàng! Đang hiển thị...")
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                frame_error_count += 1
                if frame_error_count >= max_frame_errors:
                    print(f"\nLỗi: Không thể đọc frame từ Camera {camera_id} sau {max_frame_errors} lần thử!")
                    print("Có thể camera đang bị chiếm dụng hoặc đã bị ngắt kết nối.")
                    break
                
                # Thử đọc lại sau một chút
                time.sleep(0.1)
                continue
            
            # Reset error count nếu đọc thành công
            frame_error_count = 0
        
            # Flip frame để mirror
            frame = cv2.flip(frame, 1)
            
            try:
                # Chuyển đổi BGR sang RGB
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Nhận diện tư thế
                results = detector.pose.process(rgb_frame)
            except Exception as e:
                print(f"Lỗi xử lý frame: {e}")
                continue
        
            is_straight = False
            if results.pose_landmarks:
                try:
                    # Vẽ skeleton
                    detector.mp_drawing.draw_landmarks(
                        frame,
                        results.pose_landmarks,
                        detector.mp_pose.POSE_CONNECTIONS,
                        detector.mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                        detector.mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2)
                    )
                    
                    # Kiểm tra tư thế ngồi thẳng
                    is_straight = detector.detect_sitting_straight(results.pose_landmarks)
                except Exception as e:
                    print(f"Lỗi khi vẽ skeleton: {e}")
            
            # Xử lý đếm thời gian
            current_time = time.time()
            
            if is_straight:
                if start_time is None:
                    start_time = current_time
                
                elapsed = current_time - start_time
                
                # Hiển thị thời gian đã giữ
                if elapsed >= required_time:
                    # Đã giữ đủ thời gian
                    cv2.putText(frame, "THANH CONG! Da tat bao thuc!", 
                               (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
                    cv2.putText(frame, f"Da giu tu the: {elapsed:.1f}s", 
                               (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                else:
                    # Đang đếm
                    remaining = required_time - elapsed
                    cv2.putText(frame, f"Dang giu tu the: {elapsed:.1f}s / {required_time:.1f}s", 
                               (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
                    cv2.putText(frame, f"Con lai: {remaining:.1f}s", 
                               (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
            else:
                # Không ngồi thẳng, reset đếm
                if start_time is not None:
                    start_time = None
                cv2.putText(frame, "Hay ngoi thang truoc camera!", 
                           (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            
            # Hiển thị trạng thái
            status_color = (0, 255, 0) if is_straight else (0, 0, 255)
            status_text = "NGOI THANG" if is_straight else "CHUA THANG"
            cv2.putText(frame, f"Trang thai: {status_text}", 
                       (50, frame.shape[0] - 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, status_color, 2)
            
            # Hiển thị thông tin camera
            cv2.putText(frame, f"Camera: {camera_id} | Nhan 'c' de chuyen doi", 
                       (50, frame.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            # Hiển thị frame
            try:
                cv2.imshow('Nhan dien tu the - Test', frame)
            except Exception as e:
                print(f"Lỗi hiển thị frame: {e}")
                break
            
            # Xử lý phím
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                print("\nĐang thoát...")
                break
            elif key == ord('r'):
                start_time = None
                print("Đã reset đếm")
            elif key == ord('c'):
                # Chuyển đổi camera
                cap.release()
                cameras = list_available_cameras()
                if not cameras:
                    print("Không có camera nào khác!")
                    break
                
                # Tìm camera tiếp theo
                try:
                    current_idx = cameras.index(camera_id)
                    next_idx = (current_idx + 1) % len(cameras)
                    camera_id = cameras[next_idx]
                except ValueError:
                    camera_id = cameras[0]
                
                print(f"Chuyển sang Camera {camera_id}...")
                cap = cv2.VideoCapture(camera_id)
                if not cap.isOpened():
                    print(f"Không thể mở Camera {camera_id}!")
                    break
                cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                start_time = None
                frame_error_count = 0
            elif ord('0') <= key <= ord('9'):
                # Chuyển sang camera theo số
                new_camera_id = key - ord('0')
                if new_camera_id != camera_id:
                    cap.release()
                    print(f"Đang chuyển sang Camera {new_camera_id}...")
                    cap = cv2.VideoCapture(new_camera_id)
                    if cap.isOpened():
                        ret, _ = cap.read()
                        if ret:
                            camera_id = new_camera_id
                            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                            start_time = None
                            frame_error_count = 0
                            print(f"Đã chuyển sang Camera {camera_id}")
                        else:
                            cap.release()
                            cap = cv2.VideoCapture(camera_id)
                            print(f"Camera {new_camera_id} không hoạt động, giữ nguyên Camera {camera_id}")
                    else:
                        cap = cv2.VideoCapture(camera_id)
                        print(f"Không thể mở Camera {new_camera_id}, giữ nguyên Camera {camera_id}")
    
    except KeyboardInterrupt:
        print("\n\nĐã dừng bởi người dùng (Ctrl+C)")
    except Exception as e:
        print(f"\n\nLỗi không mong đợi: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if cap.isOpened():
            cap.release()
        cv2.destroyAllWindows()
        print("Đã đóng camera và dọn dẹp tài nguyên")

if __name__ == "__main__":
    try:
        test_pose_detection()
    except ImportError:
        print("Lỗi: Cần cài đặt các thư viện sau:")
        print("  pip install opencv-python mediapipe")
    except Exception as e:
        print(f"Lỗi: {e}")


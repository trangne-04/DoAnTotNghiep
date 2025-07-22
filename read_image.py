import cv2
import numpy as np


def keep_color_and_convert_to_white(image):
    # Đọc ảnh
    # image = cv2.imread(image_path)

    # Định nghĩa khoảng màu cam trong không gian HSV
    lower_color = np.array([0, 0, 0])  # Giới hạn thấp
    upper_color = np.array([50, 255, 255])  # Giới hạn cao


    # Chuyển đổi từ BGR sang HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Tạo mặt nạ cho màu đã chỉ định
    mask = cv2.inRange(hsv, lower_color, upper_color)

    # Tạo ảnh trắng
    white_image = np.ones_like(image) * 255

    # Kết hợp giữ lại màu từ ảnh gốc và chuyển đổi các màu khác thành trắng
    result = np.where(mask[:, :, None] == 255, image, white_image)

    return result, mask


def find_largest_contour_and_draw2(result, mask):
    # Tìm các contour
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # Tìm contour lớn nhất
        largest_contour = max(contours, key=cv2.contourArea)

        # Vẽ contour lớn nhất lên ảnh kết quả
        cv2.drawContours(result, [largest_contour], -1, (0, 0, 255), 3)  # Vẽ bằng màu đỏ

        # Tính diện tích contour lớn nhất
        area = cv2.contourArea(largest_contour)
        print(f"Diện tích contour lớn nhất: {area:.2f} pixels")

    return result, area


def keep_green_and_convert_to_white(image):
    # Đọc ảnh
    # image = cv2.imread(image_path)

    # Chuyển đổi từ BGR sang HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Định nghĩa khoảng màu xanh lá cây trong không gian HSV
    lower_green = np.array([20, 0, 0])  # Giới hạn thấp
    upper_green = np.array([80, 255, 130])  # Giới hạn cao

    # Tạo mặt nạ cho màu xanh lá cây
    mask = cv2.inRange(hsv, lower_green, upper_green)

    # Tạo ảnh trắng
    white_image = np.ones_like(image) * 255

    # Kết hợp giữ lại màu xanh lá cây từ ảnh gốc và chuyển đổi các màu khác thành trắng
    result = np.where(mask[:, :, None] == 255, image, white_image)

    return result, mask


def find_largest_contour_and_draw(result, mask):
    # Tìm các contour
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # Tìm contour lớn nhất
        largest_contour = max(contours, key=cv2.contourArea)

        # Vẽ contour lớn nhất lên ảnh kết quả
        cv2.drawContours(result, [largest_contour], -1, (0, 0, 255), 3)  # Vẽ bằng màu đỏ

        # Tính diện tích contour lớn nhất
        area = cv2.contourArea(largest_contour)
        print(f"Diện tích contour lớn nhất: {area:.2f} pixels")

    return result, area


def open_external_camera(camera_index=1):
    # Mở camera (chỉ số camera ngoài)
    cap = cv2.VideoCapture(camera_index)

    if not cap.isOpened():
        print("Không thể mở camera. Kiểm tra kết nối.")
        return

    # Thiết lập độ phân giải
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # Độ rộng
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)  # Độ cao

    while True:
        # Đọc từng khung hình từ camera
        ret, frame = cap.read()

        if not ret:
            print("Không thể nhận dạng khung hình.")
            break

        classify_fruit(frame)

        # Hiển thị khung hình
        # cv2.imshow('Camera', frame)

        # Nhấn 'q' để thoát
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Giải phóng tài nguyên
    cap.release()
    cv2.destroyAllWindows()

def kich_thuoc_qua(area):
    if area < 200000 :
        result = 'Nhỏ'
    elif 200000 <= area < 300000:
        result = 'Vừa'
    else:
        result = "To"
    return result

def classify_fruit(img):
    # img = cv2.imread(image_path)

    if img is None:
        print("Không thể đọc được ảnh!")
        return

    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    green_lower = np.array([30, 60, 50])
    green_upper = np.array([80, 255, 255])

    red_lower1 = np.array([0, 50, 50])
    red_upper1 = np.array([10, 255, 255])
    red_lower2 = np.array([170, 50, 50])
    red_upper2 = np.array([180, 255, 255])

    orange_lower = np.array([10, 50, 50])
    orange_upper = np.array([25, 255, 255])

    green_mask = cv2.inRange(hsv_img, green_lower, green_upper)
    red_mask1 = cv2.inRange(hsv_img, red_lower1, red_upper1)
    red_mask2 = cv2.inRange(hsv_img, red_lower2, red_upper2)
    orange_mask = cv2.inRange(hsv_img, orange_lower, orange_upper)

    red_mask = cv2.bitwise_or(red_mask1, red_mask2)

    green_area = cv2.countNonZero(green_mask)
    red_area = cv2.countNonZero(red_mask)
    orange_area = cv2.countNonZero(orange_mask)

    total_area = green_area + red_area + orange_area

    if total_area == 0:
        print("Không phát hiện được màu đặc trưng!")
        return

    green_ratio = green_area / total_area
    red_ratio = red_area / total_area
    orange_ratio = orange_area / total_area
    area = 0
    if green_ratio > 0.5:
        result1 = "Quả xanh, "
        result, mask = keep_green_and_convert_to_white(img)
        # Vẽ contour lớn nhất lên ảnh kết quả
        result_with_largest_contour, area = find_largest_contour_and_draw(result, mask)
        kichthuoc = kich_thuoc_qua(area)
        result1 += kichthuoc
        # Hiển thị ảnh kết quả
        # cv2.imshow('Result with Largest Contour', result_with_largest_contour)

    elif red_ratio > 0.4 or orange_ratio > 0.4:
        result1 = "Quả chín, "
        result, mask = keep_color_and_convert_to_white(img)
        # Vẽ contour lớn nhất lên ảnh kết quả
        result_with_largest_contour, area = find_largest_contour_and_draw2(result, mask)
        kichthuoc = kich_thuoc_qua(area)
        result1 += kichthuoc
        # Hiển thị ảnh kết quả
        # cv2.imshow('Result with Largest Contour', result_with_largest_contour)
    else:
        result1 = "Không xác định rõ"


    return result1, area


if __name__ == '__main__':
    open_external_camera()



    # open_external_camera(camera_index=1)  # Thay đổi chỉ số nếu cần
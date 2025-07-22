import cv2
import numpy as np


def keep_color_and_convert_to_white(image_path):
    # Đọc ảnh
    image = cv2.imread(image_path)

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

    return result


if __name__ == '__main__':
    image_path = "Result with Largest Contour.png"  # Đường dẫn tới ảnh của bạn


    # Giữ lại màu cam
    result_orange, mask_orange = keep_color_and_convert_to_white(image_path)

    # Vẽ contour lớn nhất cho màu cam
    result_with_largest_contour_orange = find_largest_contour_and_draw(result_orange, mask_orange)

    # Hiển thị ảnh kết quả cho màu cam
    cv2.imshow('Result with Largest Contour (Orange)', result_with_largest_contour_orange)
    cv2.waitKey(0)  # Chờ cho đến khi có phím nhấn
    cv2.destroyAllWindows()
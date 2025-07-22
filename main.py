import datetime
import sys
import threading
import time

import cv2
import numpy as np
from PyQt5.QtCore import Qt, QTimer, QUrl, QLocale
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QTableWidgetItem
import serial

import read_image
from app_ui_manh_ui import Ui_MainWindow


class MainGUI(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()
        self.setupUi(self)
        # self.chon_anh_bt.clicked.connect(self.show_dialog)
        # self.nhan_dang_bt.clicked.connect(self.detect_yl)
        self.image = None

        self.capture = cv2.VideoCapture(1)

        # Thiết lập độ phân giải
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # Độ rộng
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)  # Độ cao

        self.frame = None

        self.timer = QTimer()
        self.timer.timeout.connect(self.show_camera)
        self.timer.start(30)  # Cập nhật mỗi 30 ms

        self.choose_cb.currentIndexChanged.connect(self.change_index_cb)

        self.nho_lb.setVisible(False)
        self.vua_lb.setVisible(False)
        self.to_lb.setVisible(False)
        self.nho_txt.setVisible(False)
        self.vua_txt.setVisible(False)
        self.to_txt.setVisible(False)
        self.serial = serial.Serial('COM3', 115200, timeout=1)
        self.stop_bit = False
        self.start_bt.clicked.connect(self.start_fc)
        self.stop_bt.clicked.connect(self.stop_fc)

        self.qua_xanh_count = 0
        self.qua_chin_count = 0
        self.qua_nho_count = 0
        self.qua_vua_count = 0
        self.qua_to_count = 0

    def change_index_cb(self):
        try:
            current_index = self.choose_cb.currentIndex()
            if current_index == 0:
                self.nho_lb.setVisible(False)
                self.vua_lb.setVisible(False)
                self.to_lb.setVisible(False)
                self.nho_txt.setVisible(False)
                self.vua_txt.setVisible(False)
                self.to_txt.setVisible(False)

                self.xanh_lb.setVisible(True)
                self.xanh_txt.setVisible(True)
                self.chin_lb.setVisible(True)
                self.chin_txt.setVisible(True)
            else:
                self.nho_lb.setVisible(True)
                self.vua_lb.setVisible(True)
                self.to_lb.setVisible(True)
                self.nho_txt.setVisible(True)
                self.vua_txt.setVisible(True)
                self.to_txt.setVisible(True)

                self.xanh_lb.setVisible(False)
                self.xanh_txt.setVisible(False)
                self.chin_lb.setVisible(False)
                self.chin_txt.setVisible(False)

        except Exception as ex:
            print(ex)

        # self.start_bt.clicked.connect(self.start_fc)
        # self.stop_bt.clicked.connect(self.stop_fc)
        # self.serial = serial.Serial(port='COM3', baudrate=115200)
        # threading_main = threading.Thread(target=self.main_thread, args=())
        # threading_main.start()

    def start_fc(self):
        try:
            # print("Start 1")
            self.stop_bit = True
            self.start_bt.setStyleSheet('background-color: red')
            threading_main = threading.Thread(target=self.main_thread, args=())
            threading_main.start()
        except Exception as ex:
            print(ex)

    def stop_fc(self):
        try:
            self.stop_bit = False
            self.start_bt.setStyleSheet('background-color: white')
        except Exception as ex:
            print(ex)

    def check_done(self):
        try:
            result_done = False

            while not result_done:
                # print("Dang cho kq")
                result_read = self.serial.readline().decode().strip().split(',')
                print(result_read)
                if result_read[0] == 'Done':
                    print("Done")
                    self.xanh_txt.setText(result_read[1])
                    self.chin_txt.setText(result_read[2])
                    self.nho_txt.setText(result_read[3])
                    self.vua_txt.setText(result_read[4])
                    self.to_txt.setText(result_read[5])

                    break



        except Exception as ex:
            print(ex)

    def main_thread(self):
        while self.stop_bit:
            try:


                result_start = self.serial.readline().decode().strip()
                if result_start == 'Start':
                    time.sleep(3)
                    class_name, area = read_image.classify_fruit(self.frame)
                    if area > 100000:
                        current_index = self.choose_cb.currentIndex()
                        if current_index == 0:
                            if class_name.split(',')[0] == 'Quả xanh':
                                print("Quả xanh")
                                self.serial.write(('Loai1' + '\n').encode())
                                self.check_done()
                                # time.sleep(1)

                                self.qua_xanh_count += 1
                            elif class_name.split(',')[0] == 'Quả chín':
                                self.serial.write(('Loai2' + '\n').encode())
                                self.check_done()
                                # time.sleep(1)

                                print("Quả chín")
                                self.qua_chin_count += 1

                        else:
                            if class_name.split(',')[1] == ' Nhỏ':
                                self.serial.write(('Loai3' + '\n').encode())
                                self.check_done()
                                # time.sleep(1)

                                self.qua_nho_count += 1

                                print("Quả Nhỏ")
                            elif class_name.split(',')[1] == ' Vừa':
                                self.serial.write(('Loai4' + '\n').encode())
                                self.check_done()
                                # time.sleep(1)

                                self.qua_vua_count += 1

                                print("Quả Vừa")
                            elif class_name.split(',')[1] == ' To':
                                self.serial.write(('Loai5' + '\n').encode())
                                self.check_done()
                                # time.sleep(1)
                                self.qua_to_count += 1

                                print("Quả To")

                time.sleep(0.2)

            except Exception as ex:
                print(ex)

    def show_camera(self):
        try:
            ret, self.frame = self.capture.read()
            if ret:
                # Chuyển đổi màu BGR sang RGB
                frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                # Chuyển đổi thành QImage
                h, w, ch = frame.shape
                bytes_per_line = ch * w
                # Giả sử self.image_txt là QLabel đã được khởi tạo
                image_txt_width = self.image_txt.width()
                image_txt_height = self.image_txt.height()

                frame = cv2.resize(frame, (image_txt_width, image_txt_height))
                # Chuyển đổi thành QImage
                h, w, ch = frame.shape
                bytes_per_line = ch * w
                q_img = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
                self.image_txt.setPixmap(QPixmap.fromImage(q_img))
        except Exception as ex:
            print(ex)

    def show_dialog(self):
        try:
            # Mở hộp thoại để chọn tệp
            options = QFileDialog.Options()
            options |= QFileDialog.ReadOnly
            file_name, _ = QFileDialog.getOpenFileName(self, "Chọn Hình Ảnh", "",
                                                       "Images (*.png *.jpg *.jpeg);;All Files (*)",
                                                       options=options)
            if file_name:
                # Hiển thị đường dẫn tệp trong QLineEdit
                self.image = cv2.imread(file_name)
                self.duong_dan_anh_txt.setText(file_name)
                h, w, ch = self.image.shape
                # frame = cv2.cvtColor(self.current_frame_bs_lan2, cv2.COLOR_BGR2RGB)
                frame = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
                bytes_per_line = ch * w
                image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(image)
                self.image_txt.setPixmap(pixmap.scaled(
                    self.image_txt.size()  # Chất lượng chuyển đổi mượt mà
                ))

        except Exception as ex:
            print(ex)

    def detect_yl(self):
        try:
            # 3. Thực hiện phân loại
            results = self.model(source=self.image, conf=0.35, save_txt=True)  # conf là ngưỡng độ tin cậy

            # 4. Xử lý và hiển thị kết quả
            for result in results:
                print(result.boxes.xyxy[0])
                if len(result.boxes.xyxy) > 0:
                    x1, y1, x2, y2 = result.boxes.xyxy[0]
                    # Vẽ hình chữ nhật
                    color = (0, 255, 0)  # Màu xanh lá cây (BGR)
                    thickness = 2  # Độ dày của đường viền
                    cv2.rectangle(self.image, (int(x1), int(y1)), (int(x2), int(y2)), color, thickness)
                    # Lấy tên lớp (giả sử class_names là danh sách tên các loại quả)
                    class_names = ['cachua', 'chuoi', 'cam']
                    class_id = int(result.boxes.cls[0])  # Lấy chỉ số lớp
                    class_name = class_names[class_id]  # Lấy tên quả từ danh sách

                    # Thêm văn bản phân loại
                    text = f"{class_name}"  # Văn bản hiển thị tên quả
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    font_scale = 0.7
                    text_color = (0, 0, 255)  # Màu đỏ (BGR)
                    text_thickness = 2
                    text_position = (int(x1), int(y1) + 20)  # Vị trí văn bản (phía trên hình chữ nhật)

                    # Vẽ văn bản lên ảnh
                    cv2.putText(self.image, text, text_position, font, font_scale, text_color, text_thickness)

            # Hiển thị đường dẫn tệp trong QLineEdit
            h, w, ch = self.image.shape
            # frame = cv2.cvtColor(self.current_frame_bs_lan2, cv2.COLOR_BGR2RGB)
            frame = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            bytes_per_line = ch * w
            image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(image)
            self.image_txt.setPixmap(pixmap.scaled(
                self.image_txt.size()  # Chất lượng chuyển đổi mượt mà
            ))
        except Exception as ex:
            print(ex)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainGUI()
    main_window.setWindowTitle('Phân loại trái cây')
    main_window.show()
    sys.exit(app.exec_())

#  The code will print the image of in local

from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel
import sys
from PyQt6.QtGui import QPixmap
from PIL import Image
import random
import requests
from io import BytesIO
import cairosvg
from PyQt6.QtSvgWidgets import QSvgWidget


class Canvas(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.setGeometry(10, 50, 480, 400)
        self.setFrameStyle(1)
        self.images = []

    def add_img(self, img_path):
        img = QPixmap(img_path)
        label = QLabel(self)
        label.setPixmap(img)
        label.move(random.randint(0, 700), random.randint(0, 450))
        label.show()
        self.images.append(label)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Geometric Image")
        self.setGeometry(400, 400, 500, 500)
        self.canvas_window = Canvas(self)
        self.canvas_window.setStyleSheet("background-color:white;")

        self.Download_button = QPushButton("Add Image", self)
        self.Download_button.setGeometry(20, 20, 200, 30)
        self.Download_button.clicked.connect(self.Download_Render_image)
    
    def Download_Render_image(self):
        image_number = random.choice(range(1, 36)) 
        image_url = "https://raw.githubusercontent.com/hfg-gmuend/openmoji/44c02495e040c52fbea0bfb1cba89aa24754f9a8/src/symbols/geometric/1F533.svg"
        response = requests.get(image_url)

        if response.status_code == 200:
            img_data = response.content
            png_data = cairosvg.svg2png(bytestring=img_data)
            img_file = BytesIO(png_data)
            img = Image.open(img_file)
            img.show()
            self.canvas_window.add_img(img_file)
        else:
            print("Failed to fetch the image")

    def closeEvent(self, event):
        for image_label in self.canvas_window.images:
            image_label.setParent(None)
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
# the second button that i made of the requirements.

import sys
import random
import os
from PyQt6.QtCore import Qt, QPoint, QRect, QSize
from PyQt6.QtGui import QImage, QColor, QPainter, QPen
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600

class GeometricImage:
    def __init__(self, image_path, position, size, color):
        self.image_path = image_path
        self.position = position
        self.size = size
        self.color = color

class Canvas(QWidget):
    def __init__(self):
        super().__init__()
        self.images = []
        self.selected_images = set()
        self.grouped_images = set()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        for image in self.images:
            painter.setPen(QPen(Qt.GlobalColor.black))
            painter.setBrush(QColor(image.color))

            image_rect = QRect(image.position, QSize(image.size.width(), image.size.height()))
            painter.drawImage(image_rect, image.image)

            if image in self.selected_images:
                painter.drawRect(image_rect)

            if image in self.grouped_images:
                painter.drawLine(image_rect.center(), self.calculateGroupCenter())


    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            for image in self.images:
                image_rect = QRect(image.position, image.size)
                if image_rect.contains(event.pos()):
                    if image in self.selected_images:
                        self.selected_images.remove(image)
                    else:
                        self.selected_images.add(image)
                    self.update()
                    break

    def calculateGroupCenter(self):
        center_x = sum(image.position.x() + image.size.width() / 2 for image in self.grouped_images) / len(self.grouped_images)
        center_y = sum(image.position.y() + image.size.height() / 2 for image in self.grouped_images) / len(self.grouped_images)
        return QPoint(center_x, center_y)

    def groupSelectedImages(self):
        if self.selected_images:
            self.grouped_images.update(self.selected_images)
            self.selected_images.clear()
            self.update()

    def downloadGeometricImage(self):
        image_number = random.choice(range(1, 36))  # Adjust the range based on the available images
        image_path = "https://raw.githubusercontent.com/hfg-gmuend/openmoji/44c02495e040c52fbea0bfb1cba89aa24754f9a8/src/symbols/geometric/1F533.svg"
        try:
            image = QImage(image_path)
            
            position = QPoint(random.randint(0, CANVAS_WIDTH - image.width()), random.randint(0, CANVAS_HEIGHT - image.height()))
            size = QRect(position, image.size())
            color = QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            geometric_image = GeometricImage(image_path, position, size, color)
            geometric_image.image = image
            self.images.append(geometric_image)
            self.update()
        except Exception as e:
            print(f"Error loading image: {e}")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Geometric Image - Second Button")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)

        self.canvas = Canvas()
        main_layout.addWidget(self.canvas)

        button_layout = QHBoxLayout()

        download_button = QPushButton("Add Image")
        download_button.clicked.connect(self.canvas.downloadGeometricImage)
        button_layout.addWidget(download_button)

        group_button = QPushButton("Group Images")
        group_button.clicked.connect(self.canvas.groupSelectedImages)
        button_layout.addWidget(group_button)

        main_layout.addLayout(button_layout)
        self.setCentralWidget(central_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

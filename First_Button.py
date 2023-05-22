# Importing the libraries that required
import sys
import random
import os
from PyQt6.QtGui import QPainter, QImage, QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QGraphicsScene, QGraphicsView, QGraphicsItem

# Canvas Window
class Canvas(QGraphicsView):
    def __init__(self):
        super().__init__()
        
        self.setScene(QGraphicsScene())
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)

        # Path of the local folder which downloaded of the github folder
        # Path to the local folder where the SVG images are stored
        self.image_folder = "A:\eSim IITB\Desktop_App\openmoji-master\openmoji-master\src\symbols\geometric"

    def addImage(self, pixmap):
        item = self.scene().addPixmap(pixmap)
        # for selecting the image
        item.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        
        # for dragging or moving the image
        item.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        item.setPos(random.randint(0, self.width()), random.randint(0, self.height()))
        self.ensureVisible(item)
    
    # picking the random image from the folder with the help of list
    def getRandomImage(self):
        svg_files = [f for f in os.listdir(self.image_folder) if f.endswith(".svg")]
        if svg_files:
            svg_file = random.choice(svg_files)
            svg_path = os.path.join(self.image_folder, svg_file)
            image = QImage(svg_path)
            pixmap = QPixmap.fromImage(image)
            return pixmap
        else:
            return None

# Mainwindow
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Geometric Image - First Button")
        self.setGeometry(100, 100, 800, 600)

        self.canvas = Canvas()
        self.setCentralWidget(self.canvas)

        # Adding of Push Button in the canvas
        button = QPushButton("Add Image", self)
        button.clicked.connect(self.addRandomImage)

    def addRandomImage(self):
        pixmap = self.canvas.getRandomImage()
        if pixmap:
            self.canvas.addImage(pixmap)

# Main
if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())

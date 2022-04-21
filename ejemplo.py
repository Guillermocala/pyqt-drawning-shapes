import sys
from PySide6 import QtWidgets, QtGui
from PySide6.QtGui import (QPainter)
from PySide6.QtWidgets import (
    QApplication, QWidget
)

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(500, 100, 500, 500)
        self.setWindowTitle("Shape drawer")
        self.show()

    def paintEvent(self, event):
        dibujo = QPainter(self)
        dibujo.drawRect(100, 15, 300, 100)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = Window()
    sys.exit(app.exec())

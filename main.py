import sys
from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtCore import Qt
from PySide6.QtGui import (
    QPixmap, QPainter, QPaintEvent, QBrush,
    QPen, QFont
)
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget,
    QLabel, QHBoxLayout, QToolBar
)

class MyApp(QMainWindow):
    def __init__(self):
        super(MyApp, self).__init__()
        self.setGeometry(300, 100, 800, 500)
        self.setWindowTitle("Shape drawer")
        self.initUI()
        self.initMenuBar()
        self.initToolbar()
        self.show()

    def initUI(self):
        self.lienzo = QLabel()
        self.pixmap = QPixmap(self.size())
        self.pixmap.fill(Qt.white)
        self.lienzo.setPixmap(self.pixmap)
        self.setCentralWidget(self.lienzo)

    def paintEvent(self, event: QPaintEvent):
        print(self.rect())

    def initMenuBar(self):
        self.menu_bar = self.menuBar()
        #opcion 1
        self.opcion1 = self.menu_bar.addMenu("File")
        self.subAction11 = self.opcion1.addAction("Save")
        self.subAction12 = self.opcion1.addAction("Load")
        self.opcion1.addSeparator()
        self.opcion1.addAction("Exit", self.close)
        #opcion2
        self.opcion2 = self.menu_bar.addMenu("Toolbar")
        self.subAction21 = self.opcion2.addAction("Option 1")
        self.subAction22 = self.opcion2.addAction("Option 2")

    def initToolbar(self):
        self.options_toolbar = QToolBar("Options1", self)
        self.addToolBar(Qt.RightToolBarArea, self.options_toolbar)
        self.options_toolbar.addAction("Draw state", lambda: self.saludo("draw state"))
        self.options_toolbar.addAction("Draw accept state", lambda: self.saludo("draw accept state"))
    
    def saludo(self, texto):
        print(texto)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MyApp()
    sys.exit(app.exec())

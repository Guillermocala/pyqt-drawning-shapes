import sys
from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtCore import Qt
from PySide6.QtGui import (
    QPixmap
)
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget,
    QLabel, QHBoxLayout
)

class MyApp(QMainWindow):
    def __init__(self):
        super(MyApp, self).__init__()
        self.setGeometry(500, 100, 500, 500)
        self.setWindowTitle("Shape drawer")
        self.initUI()
        self.initToolbar()
        self.show()

    def initUI(self):
        self.principal = QWidget()
        self.lienzo = QLabel()
        self.pixmap = QPixmap(self.principal.size())
        self.pixmap.fill(Qt.darkCyan)
        self.lienzo.setPixmap(self.pixmap)
        self.lienzo.setMask(self.pixmap.mask())
        self.principal.setLayout(self.lienzo)
        self.setCentralWidget(self.principal)

    def initToolbar(self):
        self.options_toolbar = self.addToolBar("Options")
        self.options_toolbar.addAction("Draw state", lambda: self.saludo("draw state"))
        self.options_toolbar.addAction("Draw accept state", lambda: self.saludo("draw accept state"))
    
    def saludo(self, texto):
        print(texto)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MyApp()
    sys.exit(app.exec())

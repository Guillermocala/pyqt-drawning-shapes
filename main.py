import sys
from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtCore import (
    Qt, QPoint
)
from PySide6.QtGui import (
    QPixmap, QPainter, QPaintEvent, QBrush,
    QPen, QFont, QAction
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
        # lista de puntos para dibujar
        self.points = {1:QPoint(100, 200), 2:QPoint(150, 250), 3:QPoint(200, 300)}
        print(self.points)
        self.draw = False
        self.square = False
        self.circle = False
        self.lienzo = QLabel()
        self.pixmap = QPixmap(self.size())
        self.painter = QPainter(self.pixmap)
        self.pen = QPen(Qt.black, 4, Qt.SolidLine)
        self.painter.setPen(self.pen)
        self.pixmap.fill(Qt.white)
        self.setCentralWidget(self.lienzo)

    def paintEvent(self, event: QPaintEvent):
        self.painter.drawPixmap(0, 0, self.pixmap)
        self.lienzo.setPixmap(self.pixmap)

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
        self.options_toolbar = QToolBar("Options1")
        self.addToolBar(Qt.RightToolBarArea, self.options_toolbar)
        self.options_toolbar.addAction("Draw state", self.saludo)
        self.options_toolbar.addAction("Draw accept state", self.saludo)
        self.options_toolbar.addSeparator()
        self.options_toolbar.addAction("testing")
        self.button_action = QAction("circle", self)
        self.button_action2 = QAction("square", self)
        self.button_action.triggered.connect(self.onMyToolBarButtonClick)
        self.button_action2.triggered.connect(self.onMyToolBarButtonClick)
        self.options_toolbar.addAction(self.button_action)
        self.options_toolbar.addAction(self.button_action2)
    
    def onMyToolBarButtonClick(self):
        print(self.sender().text())
        self.pen2 = QPen(Qt.red, 2, Qt.SolidLine)
        self.painter.setPen(self.pen2)
        match self.sender().text():
            case "circle":
                if self.circle:
                    self.circle = False
                    self.pixmap.fill(Qt.white)
                else:
                    # draw a accept state
                    self.painter.drawEllipse(200, 200, 50, 50)
                    self.painter.drawEllipse(195, 195, 60, 60)
                    self.circle = True
            case "square":
                if self.square:
                    self.square = False
                    self.pixmap.fill(Qt.white)
                else:
                    self.painter.drawRect(200, 200, 200, 200)
                    self.square = True

    def saludo(self):
        self.painter.setPen(self.pen)
        if self.draw:
            self.draw = False
            self.pixmap.fill(Qt.white)
        else:
            for key, value in self.points.items():
                self.painter.drawEllipse(value, 50, 50)
            self.draw = True

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MyApp()
    sys.exit(app.exec())
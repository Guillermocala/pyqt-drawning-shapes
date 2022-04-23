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
        """para deshabilitar la molesta opcion de hide toolbar cuando se da 
        click derecho, deshabilita los context menu en general"""
        self.setContextMenuPolicy(Qt.PreventContextMenu)
        self.indexState = 1
        self.main_dictionary = {0:QPoint(100, 100)}
        self.states_dictionary = {}
        self.accepted_states_dictionary = {}

    def initUI(self):
        # lista de puntos para dibujar
        self.posx = 200
        self.posy = 200
        self.points = {1:QPoint(100, 200), 2:QPoint(150, 250), 3:QPoint(200, 300)}
        print(self.points)
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
        self.subAction21 = self.opcion2.addAction("Option 1", self.toolbarShow)
        self.subAction22 = self.opcion2.addAction("Option 2")
        self.subAction21.setCheckable(True)
        self.subAction22.setCheckable(True)

    def initToolbar(self):
        self.subAction21.setChecked(True)
        self.options_toolbar = QToolBar("Options1")
        self.options_toolbar.setMovable(False)
        self.addToolBar(Qt.RightToolBarArea, self.options_toolbar)
        self.options_toolbar.addAction("Draw state", self.drawStates)
        self.options_toolbar.addAction("Draw accept state", self.drawStates)
        self.options_toolbar.addSeparator()
        self.options_toolbar.addAction("Clear screen", self.clearScreen)
        self.options_toolbar.addAction("Show data", self.showData)
    
    def toolbarShow(self):
        if self.options_toolbar.isVisible():
            self.options_toolbar.setVisible(False)
        else:
            self.options_toolbar.setVisible(True)

    def drawStates(self):
        point = QPoint((self.posx), (self.posy))
        self.posx += 50     
        match self.sender().text():
            case "Draw state":
                print("Draw state case")
                # draw a accept state
                self.main_dictionary[self.indexState] = point
                self.states_dictionary[self.indexState] = point
                self.indexState += 1
                self.painter.drawEllipse(point, 50, 50)
            case "Draw accept state":
                print("Draw accept state case")
                self.main_dictionary[self.indexState] = point
                self.accepted_states_dictionary[self.indexState] = point
                self.indexState += 1
                self.painter.drawEllipse(point, 50, 50)
                self.painter.drawEllipse(point, 60, 60)
            case _:
                print("Error option -> draw states match")
        print(self.main_dictionary)

    def clearScreen(self):
        self.main_dictionary = {0:QPoint(100, 100)}
        self.states_dictionary = {}
        self.accepted_states_dictionary = {}
        self.posx = 200
        self.pixmap.fill(Qt.white)

    def showData(self):
        print("main dict: ", self.main_dictionary)
        print("states dict: ", self.states_dictionary)
        print("accepted states dict: ", self.accepted_states_dictionary)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MyApp()
    sys.exit(app.exec())
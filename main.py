import sys
from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtCore import (
    Qt, QPoint, QPointF
)
from PySide6.QtGui import (
    QPixmap, QPainter, QPaintEvent, QBrush,
    QPen, QFont, QAction, QIcon, QCursor,
    QPainterPath, QPolygonF
)
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget,
    QLabel, QHBoxLayout, QToolBar, QComboBox, QPushButton
)

class MyApp(QMainWindow):
    def __init__(self):
        super(MyApp, self).__init__()
        self.setGeometry(300, 100, 800, 500)
        self.setWindowIcon(QIcon("graph.ico"))
        self.setWindowTitle("Shape drawer")
        "tamaños de los circulos de los estados"
        self.size_inner_circle = 25
        self.size_outer_circle = 33
        "listas de estados"
        self.main_dictionary = {0:QPoint(100, 100)}
        self.states_dictionary = {0:QPoint(100, 100)}
        self.accepted_states_dictionary = {}
        "inicializacion de componentes"
        self.initUI()
        self.initMenuBar()
        self.initTransitionsModule()
        self.initToolbar()
        self.statusBar().showMessage("Welcome to the AFND visualizer", 5000)
        self.show()
        """para deshabilitar la molesta opcion de hide toolbar cuando se da 
        click derecho, deshabilita los context menu en general"""
        self.setContextMenuPolicy(Qt.PreventContextMenu)

    def initUI(self):
        self.actual_pos = QPoint(0, 0)
        self.input = False
        self.lienzo = QLabel()
        self.pixmap = QPixmap(self.size())
        self.painter = QPainter(self.pixmap)
        self.pen = QPen(Qt.black, 4, Qt.SolidLine)
        self.painter.setPen(self.pen)
        self.painter.drawPixmap(0, 0, self.pixmap)
        self.pixmap.fill(Qt.white)
        self.setCentralWidget(self.lienzo)

    def paintEvent(self, event: QPaintEvent):
        self.lienzo.setPixmap(self.pixmap)
        if not self.statusBar().currentMessage():
            self.statusBar().setStyleSheet("background-color:#F0F0F0")

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

    "modulo para insertar las aristas o transiciones(2 combobox y un boton)"
    def initTransitionsModule(self):
        self.transitionsModule = QWidget()
        self.layoutTransitionsModule = QVBoxLayout(self.transitionsModule)
        self.layoutComboboxes = QHBoxLayout()
        self.layoutButton = QVBoxLayout()
        self.initialState = QComboBox()
        self.endingState = QComboBox()
        self.initialState.setPlaceholderText("State 1")
        self.endingState.setPlaceholderText("State 2")
        self.initialState.addItem("0")
        self.endingState.addItem("0")
        self.drawTransitionButton = QPushButton("Draw transition")
        self.drawTransitionButton.clicked.connect(self.drawTransitions)
        self.layoutComboboxes.addWidget(self.initialState)
        self.layoutComboboxes.addWidget(self.endingState)
        self.layoutButton.addWidget(self.drawTransitionButton)
        self.layoutTransitionsModule.addLayout(self.layoutComboboxes)
        self.layoutTransitionsModule.addLayout(self.layoutButton)

    def initToolbar(self):
        self.subAction21.setChecked(True)
        self.options_toolbar = QToolBar("Options1")
        self.options_toolbar.setMovable(False)
        self.addToolBar(Qt.RightToolBarArea, self.options_toolbar)
        self.draw_state_action = QAction("Draw state")
        self.draw_accept_state_action = QAction("Draw accept state")
        self.draw_transition_action = QAction("Draw transition")
        self.draw_state_action.triggered.connect(self.drawStates)
        self.draw_accept_state_action.triggered.connect(self.drawStates)
        self.draw_transition_action.triggered.connect(self.drawTransitions)
        self.options_toolbar.addAction(self.draw_state_action)
        self.options_toolbar.addAction(self.draw_accept_state_action)
        self.options_toolbar.addSeparator()
        self.options_toolbar.addWidget(self.transitionsModule)
        self.options_toolbar.addSeparator()
        self.options_toolbar.addAction("Clear screen", self.clearScreen)
        self.options_toolbar.addAction("Show data", self.showData)

    def mouseReleaseEvent(self, QMouseEvent):
        if self.input:
            self.actual_pos = self.lienzo.mapFromGlobal(QCursor.pos())
            print("la pos elegida es: ", self.actual_pos)
            self.input = False
        else:
            print("la pos cualquiera es: ", self.lienzo.mapFromGlobal(QCursor.pos()))

    def toolbarShow(self):
        if self.options_toolbar.isVisible():
            self.options_toolbar.setVisible(False)
        else:
            self.options_toolbar.setVisible(True)

    def drawStates(self):
        """el while fuerza a los eventos, haciendo que fuerce el evento del
        mouse para recoger la posicion a dibujar"""
        self.input = True
        self.draw_state_action.setEnabled(False)
        self.draw_accept_state_action.setEnabled(False)
        self.statusBar().setStyleSheet("background-color:yellow")
        self.statusBar().showMessage("STATUS:   esperando coordenadas...")
        match self.sender().text():
            case "Draw state":
                print("Draw state case")
                while self.input:
                    QtCore.QCoreApplication.processEvents()
                self.states_dictionary[len(self.main_dictionary)] = self.actual_pos
                self.painter.drawText(self.actual_pos, str(len(self.main_dictionary)))
                self.painter.drawEllipse(self.actual_pos, self.size_inner_circle, self.size_inner_circle)
                self.initialState.addItem(str(len(self.main_dictionary)))
                self.endingState.addItem(str(len(self.main_dictionary)))
                self.main_dictionary[len(self.main_dictionary)] = self.actual_pos
                self.statusBar().setStyleSheet("background-color:green")
                self.statusBar().showMessage("STATUS:   State drawed!", 2000)
            case "Draw accept state":
                print("Draw accept state case")
                while self.input:
                    QtCore.QCoreApplication.processEvents()
                self.accepted_states_dictionary[len(self.main_dictionary)] = self.actual_pos
                self.painter.drawText(self.actual_pos, str(len(self.main_dictionary)))
                self.painter.drawEllipse(self.actual_pos, self.size_inner_circle, self.size_inner_circle)
                self.painter.drawEllipse(self.actual_pos, self.size_outer_circle, self.size_outer_circle)
                self.initialState.addItem(str(len(self.main_dictionary)))
                self.endingState.addItem(str(len(self.main_dictionary)))
                self.main_dictionary[len(self.main_dictionary)] = self.actual_pos
                self.statusBar().setStyleSheet("background-color:green")
                self.statusBar().showMessage("STATUS:   Accept state drawed!", 2000)
            case _:
                print("Error option -> draw states match")
        self.draw_state_action.setEnabled(True)
        self.draw_accept_state_action.setEnabled(True)

    def drawTransitions(self):
        primerSeleccionado = self.initialState.currentText()
        segundoSeleccionado = self.endingState.currentText()
        self.statusBar().setStyleSheet("background-color:red")
        if primerSeleccionado != "" and segundoSeleccionado != "":
            path = QPainterPath()
            punto1 = QPointF(self.main_dictionary[int(primerSeleccionado)])
            punto2 = QPointF(self.main_dictionary[int(segundoSeleccionado)])
            size_arrow = 15
            if punto1 == punto2:
                if int(primerSeleccionado) in self.states_dictionary:
                    diferencia = self.size_inner_circle * 2
                    punto = QPointF(punto1.x(), punto1.y() - self.size_inner_circle)
                else:
                    diferencia = self.size_outer_circle * 2
                    punto = QPointF(punto1.x(), punto1.y() - self.size_outer_circle)
                self.painter.drawArc(punto1.x() - diferencia, punto1.y() - diferencia, diferencia, diferencia, 0 * 16, 270 * 16)
                self.painter.drawLine(punto, QPointF(punto.x() - size_arrow, punto.y() - size_arrow))
                self.painter.drawLine(punto, QPointF(punto.x() + size_arrow, punto.y() - size_arrow))
                self.statusBar().setStyleSheet("background-color:green")
                self.statusBar().showMessage("STATUS:   Transition Drawed!", 2000)
            else:
                restaPuntos = QPoint(punto1.x() - punto2.x(), punto1.y() - punto2.y())
                #cuadrante 1
                if restaPuntos.x() < 0 and restaPuntos.y() > 0:
                    path.moveTo(QPointF(punto1.x(), punto1.y() - self.size_inner_circle))
                    puntoControl1 = QPointF(punto1.x(), punto2.y())
                    path.quadTo(puntoControl1, QPointF(punto2.x() - self.size_inner_circle, punto2.y()))
                    puntoFinal = path.pointAtPercent(1)
                    self.painter.drawLine(puntoFinal, QPointF(puntoFinal.x() - size_arrow, puntoFinal.y() - size_arrow))
                    self.painter.drawLine(puntoFinal, QPointF(puntoFinal.x() - size_arrow, puntoFinal.y() + size_arrow))
                #cuadrante 2
                elif restaPuntos.x() < 0 and restaPuntos.y() < 0:
                    path.moveTo(QPointF(punto1.x() + self.size_inner_circle, punto1.y()))
                    puntoControl1 = QPointF(punto2.x(), punto1.y())
                    path.quadTo(puntoControl1, QPointF(punto2.x(), punto2.y() - self.size_inner_circle))
                    puntoFinal = path.pointAtPercent(1)
                    self.painter.drawLine(puntoFinal, QPointF(puntoFinal.x() + size_arrow, puntoFinal.y() - size_arrow))
                    self.painter.drawLine(puntoFinal, QPointF(puntoFinal.x() - size_arrow, puntoFinal.y() - size_arrow))
                #cuadrante 3
                elif restaPuntos.x() > 0 and restaPuntos.y() < 0:
                    path.moveTo(QPointF(punto1.x(), punto1.y() + self.size_inner_circle))
                    puntoControl1 = QPointF(punto1.x(), punto2.y())
                    path.quadTo(puntoControl1, QPointF(punto2.x()  + self.size_inner_circle, punto2.y()))
                    puntoFinal = path.pointAtPercent(1)
                    self.painter.drawLine(puntoFinal, QPointF(puntoFinal.x() + size_arrow, puntoFinal.y() - size_arrow))
                    self.painter.drawLine(puntoFinal, QPointF(puntoFinal.x() + size_arrow, puntoFinal.y() + size_arrow))
                #cuadrante 4
                elif restaPuntos.x() > 0 and restaPuntos.y() > 0:
                    path.moveTo(QPointF(punto1.x() - self.size_inner_circle, punto1.y()))
                    puntoControl1 = QPointF(punto2.x(), punto1.y())
                    path.quadTo(puntoControl1, QPointF(punto2.x(), punto2.y() + self.size_inner_circle))
                    puntoFinal = path.pointAtPercent(1)
                    self.painter.drawLine(puntoFinal, QPointF(puntoFinal.x() + size_arrow, puntoFinal.y() + size_arrow))
                    self.painter.drawLine(puntoFinal, QPointF(puntoFinal.x() - size_arrow, puntoFinal.y() + size_arrow))
                self.painter.drawPoint(puntoControl1)
                self.painter.drawPath(path)
                self.statusBar().setStyleSheet("background-color:green")
                self.statusBar().showMessage("STATUS:   Transition Drawed!", 2000)
        else:
            self.statusBar().showMessage("STATUS:   Debe seleccionar dos indices!", 5000)

    def clearScreen(self):
        "borramos las opciones de los combobox iterando al revés"
        for i in range(len(self.main_dictionary) + 1, 0, -1):
            self.initialState.removeItem(i)
            self.endingState.removeItem(i)
        self.main_dictionary = {0:QPoint(100, 100)}
        self.states_dictionary = {0:QPoint(100, 100)}
        self.accepted_states_dictionary = {}
        self.pixmap.fill(Qt.white)
        self.statusBar().setStyleSheet("background-color:green")
        self.statusBar().showMessage("STATUS:   Screen cleared!", 2000)

    def showData(self):
        print("\n\n\tdata\n\n")
        print("main dict: ", self.main_dictionary)
        print("states dict: ", self.states_dictionary)
        print("accepted states dict: ", self.accepted_states_dictionary)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MyApp()
    sys.exit(app.exec())
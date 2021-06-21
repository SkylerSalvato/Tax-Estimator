import sys

# Qt widgets
"""from PyQt6.QtWidgets import (QApplication, QLabel, QSizePolicy, QWidget,
    QPushButton, QToolTip, QMessageBox, QMainWindow, QSizePolicy)
from PyQt6.QtGui import QFont, QIcon, QAction

class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUi()

    def initUi(self):
        exitAct = QAction(QIcon('exit24.png'), 'Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.triggered.connect(QApplication.instance().quit)
        
        spacer = QWidget(self)
        print(spacer.expandingDirections())
        #spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.toolbar = self.addToolBar('Exit')
        self.toolbar.setMovable(False)
        self.toolbar.addWidget(spacer)
        self.toolbar.addAction(exitAct)

        self.resize(350, 250)
        self.setWindowTitle('Testing Qt')
        self.setStyleSheet("background-color: #373F47; color: white;")
        self.show()

    def closeEvent(self, event):

        reply = QMessageBox.question(self, 'Message',
                        "Are you sure to quit?", QMessageBox.StandardButton.Yes |
                        QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:

            event.accept()
        else:

            event.ignore()


if __name__ == '__main__':
    # Instantiate Qt
    app = QApplication(sys.argv)

    # Create GUI
    window = QWidget()
    window.setWindowTitle('PyQt6 App')
    window.setGeometry(100, 100, 280, 80)
    window.move(60, 15)
    helloMsg = QLabel('<h1>Hello world!</h1>', parent=window)
    helloMsg.move(60, 15)

    # Show GUI
    window.show()
 
    ex = Example()

    # Run event loop
    sys.exit(app.exec())"""
from PyQt6.QtWidgets import (QLabel, QMainWindow, QWidget, QPushButton,
    QHBoxLayout, QVBoxLayout, QApplication, QStackedWidget)
from PyQt6.QtCore import QPropertyAnimation, QRect, Qt
from PyQt6.QtGui import QCursor, QIcon

class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.stacked_widget.currentChanged.connect(self.set_button_state)
        self.next_button.clicked.connect(self.next_page)
        self.prev_button.clicked.connect(self.prev_page)


    def initUI(self):

        self.next_button = QPushButton('Next')
        self.next_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.prev_button = QPushButton('Previous')
        self.prev_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.next_button.setEnabled(False)
        self.prev_button.setEnabled(False)
        tab_container = QWidget(self)
        tools_container = QWidget(self)
        tools_container.setStyleSheet("background-color: #1B1F23")
        tab_container.setStyleSheet("background-color: #23292E")

        self.stacked_widget = QStackedWidget()

        tabs = QVBoxLayout(tab_container)
        tabs.setSpacing(0)
        self.next_button.setFixedWidth(80)
        self.prev_button.setFixedWidth(80)
        tabs.addWidget(self.next_button)
        tabs.addWidget(self.prev_button)
        

        main = QHBoxLayout()
        main.addWidget(tab_container)
        main.addWidget(self.stacked_widget)
        main.setSpacing(10)

        close = QPushButton('')
        close.setIcon(QIcon('exit24.png'))
        close.clicked.connect(QApplication.instance().quit)

        toolbar = QHBoxLayout(tools_container)
        toolbar.setAlignment(Qt.AlignmentFlag.AlignRight)
        toolbar.addWidget(close)

        screen = QVBoxLayout()
        screen.addWidget(tools_container)
        screen.addLayout(main)
        screen.setSpacing(0)
        screen.setContentsMargins(0,0,0,0)

        self.setLayout(screen)
        tab_container.setStyleSheet("QPushButton { background-color: #373F47; color: white; border: none; padding: 3px; height: 50%;}"
                            "QPushButton:hover { background-color: #47525C; }"
                            "QPushButton:pressed { background-color: #505C68;}"
                            "QPushButton:disabled { color: #373F47;}")
    
        self.setStyleSheet("QWidget {background-color: #373F47; color: white;}")


    def set_button_state(self, index):
        self.prev_button.setEnabled(index > 0)
        n_pages = len(self.stacked_widget)
        self.next_button.setEnabled( index % n_pages < n_pages - 1)

    def insert_page(self, widget, index=-1):
        self.stacked_widget.insertWidget(index, widget)
        self.set_button_state(self.stacked_widget.currentIndex())

    def next_page(self):
        new_index = self.stacked_widget.currentIndex()+1
        if new_index < len(self.stacked_widget):
            self.stacked_widget.setCurrentIndex(new_index)

    def prev_page(self):
        new_index = self.stacked_widget.currentIndex()-1
        if new_index >= 0:
            self.stacked_widget.setCurrentIndex(new_index)

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    for i in range(5):
        ex.insert_page(QLabel(f'This is page {i+1}'))
    ex.resize(800,600)
    ex.show()
    app.exec()
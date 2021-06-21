import sys

# Qt widgets
from PyQt6.QtWidgets import (QLabel, QMainWindow, QWidget, QPushButton,
    QHBoxLayout, QVBoxLayout, QApplication, QStackedWidget)
from PyQt6.QtCore import QPoint, QPropertyAnimation, QRect, Qt
from PyQt6.QtGui import QCursor, QIcon

# Main Window
class TaxGui(QWidget):

    # Call Parent, remove frames, and create signals
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.stacked_widget.currentChanged.connect(self.set_button_state)
        self.next_button.clicked.connect(self.next_page)
        self.prev_button.clicked.connect(self.prev_page)

    # Setup the application parts
    def initUI(self):
        
        # Create the widgets
        self.next_button = QPushButton('Next')
        self.prev_button = QPushButton('Previous')
        close = QPushButton('')
        self.stacked_widget = QStackedWidget()
        
        # Configure the widgets
        self.next_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.next_button.setEnabled(False)
        self.prev_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.prev_button.setEnabled(False)
        #close.setIcon(QIcon('exit24.png'))
        close.clicked.connect(QApplication.instance().quit)

        # Containers for layout styling
        tab_container = QWidget(self)
        tools_container = QWidget(self)

        # Page navigation tabs initilization and configuring
        tabs = QVBoxLayout(tab_container)
        tabs.setSpacing(0)
        tabs.setContentsMargins(0,0,0,0)
        self.next_button.setFixedWidth(100)
        self.prev_button.setFixedWidth(100)

        # Add to page navigation tabs
        tabs.addWidget(self.next_button)
        tabs.addWidget(self.prev_button)
        tabs.addStretch(1)
        
        # Add to main content pages
        main = QHBoxLayout()
        main.addWidget(tab_container)
        main.addWidget(self.stacked_widget)
        main.setSpacing(10)

        # Toolbar initialization and configuring
        toolbar = QHBoxLayout(tools_container)
        toolbar.setAlignment(Qt.AlignmentFlag.AlignRight)
        toolbar.setContentsMargins(0,0,0,0)

        # Add to toolbar
        toolbar.addWidget(close)

        # Everything's layout initialization and configuring
        screen = QVBoxLayout()
        screen.setSpacing(0)
        screen.setContentsMargins(0,0,0,0)

        # Add to entire page
        screen.addWidget(tools_container)
        screen.addLayout(main)
        
        # Define app layout
        self.setLayout(screen)

        # StyleSheets
        tab_container.setStyleSheet( "QWidget { background-color: #23292E;}"
                            "QPushButton { background-color: #23292E; color: white; border: none; padding: 3px; height: 50%;}"
                            "QPushButton:hover { background-color: #47525C; }"
                            "QPushButton:pressed { background-color: #505C68;}"
                            "QPushButton:disabled { color: #373F47;}")
        
        tools_container.setStyleSheet("QWidget { background-color: #1B1F23;}"
                            #"QPushButton { background-color: #1B1F23; border: none; padding: 3px; height: 32px; width: 32px;}"
                            "QPushButton { background-image: url('exit24.png'); border: none; width: 24px; height: 24px;}"
                            "QPushButton:hover { background-color: #47525C; }"
                            "QPushButton:pressed { background-color: #505C68;}")
    
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

    def mousePressEvent(self, event):
        self.oldPos = event.globalPosition()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPosition().toPoint() - self.oldPos.toPoint())
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPosition()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    tg = TaxGui()
    for i in range(5):
        tg.insert_page(QLabel(f'This is page {i+1}'))
    tg.resize(800,600)
    tg.show()
    app.exec()
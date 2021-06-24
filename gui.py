import sys

from modules import Calculator

# Qt widgets
from PyQt6.QtWidgets import (QFrame, QScrollArea, QGroupBox, QHBoxLayout, QVBoxLayout, 
    QApplication, QStackedWidget, QSizePolicy, 
    QWidget, QLabel, QLineEdit, QPushButton, QRadioButton, QButtonGroup)
from PyQt6.QtCore import QPoint, QPropertyAnimation, QRect, Qt
from PyQt6.QtGui import QCursor, QIcon

# Main Window
class TaxGui(QWidget):

    # Call Parent, remove frames, and create signals
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setWindowTitle('Tax Estimator') 

        # Signals
        self.stacked_widget.currentChanged.connect(self.set_button_state)
        self.info.clicked.connect(self.saveInfo)
        self.income.clicked.connect(self.saveIncome)
        self.deductions.clicked.connect(self.saveDeductions)
        self.credits.clicked.connect(self.saveCredits)
        self.results.clicked.connect(self.calcResults)
        self.closer.clicked.connect(QApplication.instance().quit)

        # Add pages
        self.page_info = Info()
        self.page_income = Income()
        self.page_deductions = Deductions()
        self.insert_page(self.page_info)
        self.insert_page(self.page_income)
        self.insert_page(self.page_deductions)
        for i in range(2):
            self.insert_page(QLabel(f'test {i+1}'))

    # Setup the application parts
    def initUI(self):
        # Create the widgets
        self.info = QPushButton('Info')
        self.income = QPushButton('Income')
        self.deductions = QPushButton('Deductions')
        self.credits = QPushButton('Credits')
        self.results = QPushButton('View Results')
        self.closer = QPushButton('')
        self.stacked_widget = QStackedWidget()
        self.title = QLabel('Skyler\'s Tax Estimator!')

        # Buttons list
        buttons = [self.info, self.income, self.deductions, self.credits, self.results]        

        # Containers for layout styling
        tab_container = QWidget(self)
        self.tools_container = QWidget(self)

        # Page navigation tabs initilization and configuring
        tabs = QVBoxLayout(tab_container)
        tabs.setSpacing(0)
        tabs.setContentsMargins(0,0,0,0)

        # Button special config
        for btn in buttons:
            btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            btn.setEnabled(False)
            btn.setFixedWidth(100)
            tabs.addWidget(btn)

        # Add stretch to page navigation tabs
        tabs.addStretch(1)
        
        # Add to main content pages
        main = QHBoxLayout()
        main.addWidget(tab_container)
        main.addWidget(self.stacked_widget)
        main.setSpacing(10)

        # Toolbar initialization and configuring
        toolbar = QHBoxLayout(self.tools_container)
        toolbar.setContentsMargins(0,0,0,0)

        # Add to toolbar
        toolbar.addStretch(1)
        toolbar.addWidget(self.title)
        toolbar.addStretch(1)
        toolbar.addWidget(self.closer)

        # Everything's layout initialization and configuring
        screen = QVBoxLayout()
        screen.setSpacing(0)
        screen.setContentsMargins(0,0,0,0)

        # Add to entire page
        screen.addWidget(self.tools_container)
        screen.addLayout(main)
        
        # Define app layout
        self.setLayout(screen)

        # StyleSheets
        tab_container.setStyleSheet( "QWidget { background-color: #23292E;}"
                            "QPushButton { background-color: #23292E; color: white; border: none; padding: 3px; height: 50%;}"
                            "QPushButton:hover { background-color: #47525C; }"
                            "QPushButton:pressed { background-color: #9792E3;}"
                            "QPushButton:disabled { background-color: #373F47; border-left-style: inset; border-left-width: 5px; border-left-color: #847DDE;}")
        
        self.tools_container.setStyleSheet("QWidget { background-color: #1B1F23;}"
                            "QPushButton { background-image: url('exit24.png'); border: none; width: 24px; height: 24px;}"
                            "QPushButton:hover { background-color: #47525C; }"
                            "QPushButton:pressed { background-color: #505C68;}")
    
        self.setStyleSheet("QWidget {background-color: #373F47; color: white;}")

    # Disable button of current index
    def set_button_state(self, index):
        switcher = {
            0 : self.info,
            1 : self.income,
            2 : self.deductions,
            3 : self.credits,
            4 : self.results
        }
        for k in switcher:
            switcher[k].setEnabled(True)
        btn = switcher.get(index)
        btn.setEnabled(False)

    # Helper to add pages to end of list
    def insert_page(self, widget, index=-1):
        self.stacked_widget.insertWidget(index, widget)

    # Method that switches pages
    def goto_page(self, page=0):
        switcher = {
            0 : self.info,
            1 : self.income,
            2 : self.deductions,
            3 : self.credits
        }
        for k in switcher:
            if (switcher[k].isEnabled() == False):
                if (k == 0):
                    self.page_info.save()
                elif (k == 1):
                    print()
                elif (k == 2):
                    print()
                elif (k == 3):
                    print()
        """if (page == 4):
            # Initialize Calculator
            calc = Calculator.Calculator()
            # Run functions
            calc.fillSE()
            calc.fillSch1()
            calc.fillSch2()
            calc.fillSchD()
            calc.calcAdjIncome()
            calc.fill8995()
            calc.adjustTax()
            calc.calcStateTax()
            calc.fill8863()
            calc.fill1040()
            calc.fillState()
            res = calc.getFields()
            grand_total = int(res["self.refund_owe_total"] + res["self.st_refund_owe_total"])
            # Set text values and colors. 
            """
        self.stacked_widget.setCurrentIndex(page)
        

    # Used to move app since no frame
    def moveWindow(self, event):
        delta = QPoint(event.globalPosition().toPoint() - self.oldPos.toPoint())
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPosition()

    # Used to identify mouse location when clicked
    def mousePressEvent(self, event):
        self.tools_container.mouseMoveEvent = self.moveWindow
        self.oldPos = event.globalPosition()

    def saveInfo(self):
        self.goto_page(page=0)

    def saveIncome(self):
        self.goto_page(page=1)

    def saveDeductions(self):
        self.goto_page(page=2)

    def saveCredits(self):
        self.goto_page(page=3)

    def calcResults(self):
        self.goto_page(page=4)


# Custom label and text field
class LabeledText(QHBoxLayout):
    def __init__(self, text_field, lab):
        super().__init__()
        self.setupUI(text_field, lab)

    def setupUI(self, text_field, lab='Update Text'):
        self.setSpacing(10)
        self.addStretch()
        self.addWidget(QLabel(str(lab + ':')))
        self.addWidget(QLineEdit(text_field))
        self.itemAt(2).widget().setFixedWidth(130)
        self.addStretch()

    def GetValue(self):
        value = ''
        for i in range(0,4):
            if isinstance(self.itemAt(i).widget(), QLineEdit):
                value = self.itemAt(i).widget().text()
        return value

# Info Page
class Info(QWidget):
    def __init__(self):
        super().__init__()
        # Run setup
        self.setupUI()
    
    def setupUI(self):
        # Variables
        layout = QVBoxLayout()
        radio_box = QHBoxLayout()
        filing_status = QGroupBox('Filing status')
        self.group = QButtonGroup(radio_box)
        sng = QRadioButton('Single')
        mrd = QRadioButton('Married')

        layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        radio_box.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        radio_box.setSpacing(10)
        filing_status.setFixedSize(200, 100)
        sng.setChecked(True)

        self.group.addButton(sng)
        self.group.addButton(mrd)
        radio_box.addWidget(sng)
        radio_box.addWidget(mrd)
        filing_status.setLayout(radio_box)
        layout.addSpacing(50)
        layout.addWidget(filing_status)
        layout.addStretch(1)
        self.setLayout(layout)
        
        # Style Sheet
        self.setStyleSheet("QGroupBox { border: 2px solid gray; border-radius: 3px; margin-top: 10px; }"
                            "QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; padding: 0 15px;  }"
                            )

    def save(self):
        if (not self.group.checkedButton() is None):
            married = False if self.group.checkedButton().text() == 'Single' else True
            upd = {
                "self.married" : married
            }
            # Update fields
            Calculator.Calculator.updateFields(upd)



# Income Page
class Income(QScrollArea):
    def __init__(self):
        super().__init__()
        # Setup scrollarea
        self.setWidgetResizable(True)
        self.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Fixed)
        self.setMinimumHeight(100)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.setFrameShape(QFrame.Shape.NoFrame)
        # Run setup
        self.setupUI()

    def setupUI(self):
        # Variables
        container = QWidget()
        layout = QVBoxLayout(container)
        box1 = LabeledText('test', 'Testing')
        save = QPushButton()

        # Configure button
        save.setFixedWidth(130)
        save.setFixedHeight(45)
        save.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        # Style Sheet
        self.setStyleSheet("QPushButton { border: none; background-color: #23292E; }"
                            "QPushButton:hover { background-color: #47525C; }"
                            "QPushButton:pressed { background-color: #9792E3; }"
                            "QScrollBar:vertical { width:15px; background: #373F47; border:none } "
                            "QScrollBar::handle:vertical { background-color: #847DDE; }"
                            "QScrollBar::handle:vertical:hover { background-color: #9792E3; }"
                            "QScrollBar::sub-line:vertical, QScrollBar::add-line:vertical { background:none; }"
                            "QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background:none; }"
        )

        # Configure Page
        layout.setSpacing(15)
        layout.addLayout(box1)
        layout.addLayout(LabeledText('test', 'Testing'))
        layout.addWidget(save)
        layout.addStretch(1)

        # Contain layout in widget
        self.setWidget(container)        

class Deductions(QWidget):
    def __init__(self):
        super().__init__()
        # Run setup
        self.setupUI()
    
    def setupUI(self):
        # Variables
        layout = QVBoxLayout()
        radio_box = QHBoxLayout()
        rbox = QGroupBox('Deduction Type')
        self.group = QButtonGroup(radio_box)
        choice1 = QRadioButton('Standard Deduction')
        choice2 = QRadioButton('Itemized Deduction')
        self.std_deduction = LabeledText('12550', 'Current Standard Deduction')
        

        layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        radio_box.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        radio_box.setSpacing(10)
        rbox.setFixedSize(300, 100)
        choice1.setChecked(True)

        self.group.addButton(choice1)
        self.group.addButton(choice2)
        radio_box.addWidget(choice1)
        radio_box.addWidget(choice2)
        rbox.setLayout(radio_box)
        layout.addSpacing(50)
        layout.addWidget(rbox)
        layout.addLayout(self.std_deduction)
        layout.addSpacing(25)
        layout.addStretch(1)
        self.setLayout(layout)
        
        # Style Sheet
        self.setStyleSheet("QGroupBox { border: 2px solid gray; border-radius: 3px; margin-top: 10px; }"
                            "QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; padding: 0 15px;  }"
                            )

    def save(self):
        if (not self.group.checkedButton() is None):
            married = False if self.group.checkedButton().text() == 'Single' else True
            upd = {
                "self.STD_DEDUCTION" : float(self.std_deduction.GetValue()),
                "self.GA_DEDUCTION" : float(self.ga_deduction.Getvalue()),
                "self.GA_EXEMPT" : float(self.ga_exemption.GetValue())
            }
            # Update fields
            Calculator.Calculator.updateFields(upd)

class Credits(QWidget):
    pass

class Results(QWidget):
    pass

# Main method
if __name__ == '__main__':
    app = QApplication(sys.argv)
    tg = TaxGui()
    tg.resize(800,600)
    tg.show()
    app.exec()

"""
Pages Needed:
    Info
        Filing Status (Single, Married), Dependents
    Income
        W-2 Wages, Federal Tax Witheld, State Tax Witheld
        1099-INT Box 1, 1099-DIV Box 1a (Ordinary), 1099-DIV Box 1b (Qualified),
        Short-term Gains, Long-term Gains, Qualified Distributions,
        1099-NEC Wages, Unemployment
    Deductions
        Deduction Type (Standard, Itemized),
        Standard Deduction (Federal, State), State Exemption
    Credits
        Eligible American Opportunity Credit Costs,
        Recovery Rebate Credit
    Results
        Federal Return
        State Return
        Total Return
"""
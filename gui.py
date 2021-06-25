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
        self.page_credits = Credits()
        self.page_results = Results()
        self.insert_page(self.page_info)
        self.insert_page(self.page_income)
        self.insert_page(self.page_deductions)
        self.insert_page(self.page_credits)
        self.insert_page(self.page_results)

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
                    self.page_income.save()
                elif (k == 2):
                    self.page_deductions.save()
                elif (k == 3):
                    self.page_credits.save()
        if (page == 4):
            self.page_results.run()
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

    def text(self):
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
        hbox = QHBoxLayout()
        self.wages = QLineEdit('0')
        self.fed_tax_witheld = QLineEdit('0')
        self.st_tax_witheld = QLineEdit('0')
        self.int_field = LabeledText('0', '1099-INT Box 1')
        self.div_field = LabeledText('0', '1099-DIV Box 1a (Ordinary)')
        self.div2_field = LabeledText('0', '1099-DIV Box 1b (Qualified)')
        self.short_field = LabeledText('0', 'Short-term Gains')
        self.long_field = LabeledText('0', 'Long-term Gains')
        self.distributions = LabeledText('0', 'Qualified Distributions')
        self.nec_field = LabeledText('0', '1099-NEC Wages')
        self.unemploy_field = LabeledText('0', 'Unemployment Checks')
        
        hbox.addWidget(QLabel('W-2 Wages:'))
        hbox.addWidget(self.wages)
        hbox.addSpacing(25)
        hbox.addWidget(QLabel('Federal Tax Witheld:'))
        hbox.addWidget(self.fed_tax_witheld)
        hbox.addSpacing(25)
        hbox.addWidget(QLabel('State Tax Witheld:'))
        hbox.addWidget(self.st_tax_witheld)            

        # Configure Page
        #layout.setSpacing(15)
        layout.addSpacing(50)
        layout.addLayout(hbox)
        layout.addSpacing(25)
        layout.addLayout(self.int_field)
        layout.addSpacing(25)
        layout.addLayout(self.div_field)
        layout.addSpacing(25)
        layout.addLayout(self.div2_field) 
        layout.addSpacing(25)
        layout.addLayout(self.short_field)
        layout.addSpacing(25)
        layout.addLayout(self.long_field)
        layout.addSpacing(25)
        layout.addLayout(self.distributions) 
        layout.addSpacing(25)
        layout.addLayout(self.nec_field)
        layout.addSpacing(25)
        layout.addLayout(self.unemploy_field)
        layout.addStretch(1)

        # Contain layout in widget
        self.setWidget(container)     

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

    def save(self):
        upd = {
            "self.wages" : float(self.wages.text()),
            "self.fed_tax_witheld" : float(self.fed_tax_witheld.text()),
            "self.st_tax_witheld" : float(self.st_tax_witheld.text()),
            "self.int_income" : float(self.int_field.text()),
            "self.div_ordinary" : float(self.div_field.text()),
            "self.div_qualified" : float(self.div2_field.text()),
            "self.short_gains" : float(self.short_field.text()),
            "self.long_gains" : float(self.long_field.text()),
            "self.cap_distributions" : float(self.distributions.text()),
            "self.nec_total" : float(self.nec_field.text()),
            "self.unemployment_income" : float(self.unemploy_field.text())
        }
        Calculator.Calculator.updateFields(upd)

class Deductions(QWidget):
    def __init__(self):
        super().__init__()
        # Run setup
        self.setupUI()
    
    def setupUI(self):
        # Variables
        container = QHBoxLayout()
        layout = QVBoxLayout()
        radio_box = QHBoxLayout()
        rbox = QGroupBox('Deduction Type')
        self.group = QButtonGroup(radio_box)
        choice1 = QRadioButton('Standard Deduction')
        choice2 = QRadioButton('Itemized Deduction')
        self.std_deduction = LabeledText('12550', 'Current Standard Deduction')
        self.ga_deduction = LabeledText('4600', 'GA Standard Deduction')
        self.ga_exemption = LabeledText('2700', 'GA Exemption')
        title1 = QLabel('Standard Deduction:')
        title2 = QLabel('Itemized Deduction')
        
        radio_box.setSpacing(10)
        rbox.setFixedSize(300, 100)
        choice1.setChecked(True)
        title1.setAlignment(Qt.AlignmentFlag.AlignLeft)
        title2.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Buttons
        self.group.addButton(choice1)
        self.group.addButton(choice2)
        radio_box.addWidget(choice1)
        radio_box.addWidget(choice2)
        rbox.setLayout(radio_box)
        container.addWidget(rbox)

        layout.addSpacing(50)
        layout.addLayout(container)
        layout.addSpacing(25)
        layout.addWidget(title1)
        layout.addLayout(self.std_deduction)
        layout.addSpacing(25)
        layout.addLayout(self.ga_deduction)
        layout.addSpacing(25)
        layout.addLayout(self.ga_exemption)
        layout.addSpacing(25)
        layout.addWidget(title2)
        layout.addStretch(1)
        self.setLayout(layout)
        
        # Style Sheet
        self.setStyleSheet("QGroupBox { border: 2px solid gray; border-radius: 3px; margin-top: 10px; }"
                            "QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; padding: 0 15px;  }"
                            )

    def save(self):
        if (not self.group.checkedButton() is None):
            # Add line that sets a variable to check if using standard deduction or not
            upd = {
                "self.STD_DEDUCTION" : float(self.std_deduction.text()),
                "self.GA_DEDUCTION" : float(self.ga_deduction.text()),
                "self.GA_EXEMPT" : float(self.ga_exemption.text())
            }
            # Update fields
            Calculator.Calculator.updateFields(upd)

class Credits(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        my_sizer = QVBoxLayout()
        self.education_credit = LabeledText('0', 'Eligible American Opportunity Credit Expenses')
        self.recovery_credit = LabeledText('0', 'Recovery Rebate Credit')
        
        my_sizer.addSpacing(50)
        my_sizer.addLayout(self.education_credit)
        my_sizer.addSpacing(50)
        my_sizer.addLayout(self.recovery_credit)
        my_sizer.addStretch(1)

        self.setLayout(my_sizer)

    def save(self):
        upd = {
            "self.edu_expenses" : float(self.education_credit.text()),
            "self.stimulus_credit" : float(self.recovery_credit.text())
        }
        Calculator.Calculator.updateFields(upd)

class Results(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        my_sizer = QVBoxLayout()
        self.fed = QHBoxLayout()
        self.fed_total = QLabel(self)
        self.state = QHBoxLayout()
        self.st_total = QLabel(self)
        self.tot = QHBoxLayout()
        self.total = QLabel(self)
        self.est_payments = QHBoxLayout()
        self.monthly = QLabel(self)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setFrameShadow(QFrame.Shadow.Plain)
        sep.setLineWidth(1)
        sep.setFixedWidth(500)
        sep.setStyleSheet("color: #847DDE;")

        self.fed.addWidget(QLabel('<h1>Federal Return:</h1>\t'))
        self.fed.addWidget(self.fed_total)
        self.state.addWidget(QLabel('<h1>State Return:</h1>\t'))
        self.state.addWidget(self.st_total)
        self.tot.addWidget(QLabel('<h1>Total Return:</h1>\t'))
        self.tot.addWidget(self.total)
        self.est_payments.addWidget(QLabel('<h2>Estimated Payments Required?</h2>\t'))
        self.est_payments.addWidget(self.monthly)

        my_sizer.addSpacing(50)
        my_sizer.addLayout(self.fed)
        my_sizer.addSpacing(50)
        my_sizer.addLayout(self.state)
        my_sizer.addSpacing(50)
        my_sizer.addLayout(self.tot)
        my_sizer.addSpacing(25)
        my_sizer.addWidget(sep)
        my_sizer.addSpacing(25)
        my_sizer.addLayout(self.est_payments)
        my_sizer.addStretch(1)

        my_sizer.setAlignment(self.fed, Qt.AlignmentFlag.AlignHCenter)
        my_sizer.setAlignment(self.state, Qt.AlignmentFlag.AlignHCenter)
        my_sizer.setAlignment(self.tot, Qt.AlignmentFlag.AlignHCenter)
        my_sizer.setAlignment(self.est_payments, Qt.AlignmentFlag.AlignHCenter)
        my_sizer.setAlignment(sep, Qt.AlignmentFlag.AlignHCenter)
        

        self.setLayout(my_sizer)

    def run(self):
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
        calc.calcEstPayments()
        res = calc.getFields()
        grand_total = int(res["self.refund_owe_total"] + res["self.st_refund_owe_total"])
        # Set text values and colors. 
        self.fed_total.setText(f'<h1>${str(abs(int(res["self.refund_owe_total"])))}</h1>')
        self.st_total.setText(f'<h1>${str(abs(int(res["self.st_refund_owe_total"])))}</h1>')
        self.total.setText(f'<h1>${str(abs(grand_total))}</h1>')
        if (res["self.req_payments"] == True):
            self.monthly.setText(f'<h2>Yes, ${str(int(res["self.est_payments"]))}</h2>')
            self.monthly.setStyleSheet("color: #DB5461")
        else:
            self.monthly.setText(f'<h2>No! Estimate is ${str(int(res["self.est_payments"]))}</h2>')
            self.monthly.setStyleSheet("color: #ACE894")
        if res["self.refund_owe_total"] < 0:
            self.fed_total.setStyleSheet("color: #DB5461")
        else:
            self.fed_total.setStyleSheet("color: #ACE894")
        if res["self.st_refund_owe_total"] < 0:
            self.st_total.setStyleSheet("color: #DB5461")
        else:
            self.st_total.setStyleSheet("color: #ACE894")
        if grand_total < 0:
            self.total.setStyleSheet("color: #DB5461")
        else:
            self.total.setStyleSheet("color: #ACE894")

# Main method
if __name__ == '__main__':
    app = QApplication(sys.argv)
    tg = TaxGui()
    tg.resize(800,600)
    tg.show()
    app.exec()
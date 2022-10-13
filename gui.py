from cgitb import handler, text
import sys
import os

from modules import Calculator

# Qt widgets
from PySide6.QtWidgets import (QFrame, QScrollArea, QGroupBox, QHBoxLayout, QVBoxLayout, 
    QApplication, QStackedWidget, QSizePolicy, 
    QWidget, QLabel, QLineEdit, QPushButton, QRadioButton, QButtonGroup, QCheckBox)
from PySide6.QtCore import Property, QPoint, QPointF, QPropertyAnimation, QRectF, QEasingCurve, QSequentialAnimationGroup, QSize, QDir, Qt, Slot, Signal
from PySide6.QtGui import QCursor, QIcon, QPaintEvent, QPen, QPainter, QBrush, QColor, QFontDatabase

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
        tab_container = QWidget(self, objectName='tabContainer')
        self.tools_container = QWidget(self, objectName='toolsContainer')

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
    def __init__(self, text_field, lab, tooltip_text=None):
        super().__init__()
        self.setupUI(text_field, tooltip_text, lab)

    def setupUI(self, text_field, tooltip_text, lab='Update Text'):
        self.setSpacing(10)
        self.addStretch()
        label = QLabel(str(lab + ':'))
        label.setMinimumWidth(320)
        self.addWidget(label)
        line_edit = QLineEdit(text_field)
        line_edit.setToolTip(tooltip_text)
        self.addWidget(line_edit)
        self.itemAt(2).widget().setFixedWidth(130)
        self.addStretch()

    def text(self):
        value = ''
        for i in range(0,4):
            if isinstance(self.itemAt(i).widget(), QLineEdit):
                value = self.itemAt(i).widget().text()
        return value

class AnimatedSwitch(QCheckBox):

    _transparent_pen = QPen(Qt.GlobalColor.transparent)
    _handle_pen = QPen(Qt.GlobalColor.lightGray)

    def __init__(self, parent=None, initial_state=False):
        super().__init__(parent)
        bar_color = '#23292E'
        checked_color = '#9792E3'
        pulse_unchecked_color = '#44999999'
        handle_color = '#9792E3'
        # Save our properties on the object via self, so we can access them later
        # in the paintEvent.
        self._bar_brush = QBrush(bar_color)
        self._bar_checked_brush = QBrush(bar_color)

        self._handle_brush = QBrush(handle_color)
        self._handle_checked_brush = QBrush(QColor(checked_color))

        self._pulse_unchecked_animation = QBrush(QColor(pulse_unchecked_color))
        self._pulse_checked_animation = QBrush(QColor(pulse_unchecked_color))

        # Setup the rest of the widget.
        self.setContentsMargins(8, 0, 8, 0)
        self._handle_position = 0 if not initial_state else 1

        self._pulse_radius = 0

        self.animation = QPropertyAnimation(self, b'handle_position', self)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self.animation.setDuration(200)  # time in ms

        self.pulse_anim = QPropertyAnimation(self, b'pulse_radius', self)
        self.pulse_anim.setDuration(350)  # time in ms
        self.pulse_anim.setStartValue(10)
        self.pulse_anim.setEndValue(20)

        self.animations_group = QSequentialAnimationGroup()
        self.animations_group.addAnimation(self.animation)
        self.animations_group.addAnimation(self.pulse_anim)

        self.setMaximumWidth(75)
        self.setChecked(initial_state)
        self.stateChanged.connect(self.setup_animation)        
    
    def sizeHint(self):
        return QSize(58, 45)

    def hitButton(self, pos: QPoint):
        return self.contentsRect().contains(pos)
    
    @Slot(int)
    def setup_animation(self, value):
        self.animations_group.stop()
        if value:
            self.animation.setEndValue(1)
        else:
            self.animation.setEndValue(0)
        self.animations_group.start()
    
    def paintEvent(self, e: QPaintEvent):
        contRect = self.contentsRect()
        handleRadius = round(0.24 * contRect.height())
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        p.setPen(self._transparent_pen)
        barRect = QRectF(0, 0, contRect.width() - handleRadius, 0.40 * contRect.height())
        barRect.moveCenter(contRect.center())
        rounding = barRect.height() / 2
        
        trailLength = contRect.width() - 2 * handleRadius
        xPos = contRect.x() + handleRadius + trailLength * self._handle_position

        if self.pulse_anim.state() == QPropertyAnimation.State.Running:
            p.setBrush(
                self._pulse_checked_animation if self.isChecked() else self._pulse_unchecked_animation
            )
            p.drawEllipse(QPointF(xPos, barRect.center().y()), self._pulse_radius, self._pulse_radius)

        if self.isChecked():
            p.setBrush(self._bar_checked_brush)
            p.drawRoundedRect(barRect, rounding, rounding)
            p.setBrush(self._handle_checked_brush)
        else:
            p.setBrush(self._bar_brush)
            p.drawRoundedRect(barRect, rounding, rounding)
            p.setPen(self._handle_pen)
            p.setBrush(self._handle_brush)

        p.drawEllipse(QPointF(xPos, barRect.center().y()), handleRadius, handleRadius)

        p.end()

    @Property(float)
    def handle_position(self):
        return self._handle_position

    @handle_position.setter
    def handle_position(self, pos):
        self._handle_position = pos
        self.update()

    @Property(float)
    def pulse_radius(self):
        return self._pulse_radius

    @pulse_radius.setter
    def pulse_radius(self, pos):
        self._pulse_radius = pos
        self.update()
    
class AnimatedSwitchBox(QHBoxLayout):
    def __init__(self, optionA, optionB, initial_state=False):
        super().__init__()
        self.setupUI(initial_state, optionA, optionB)
        self._optionA = optionA
        self._optionB = optionB
    
    def toggleBoldText(self):
        if self.checkbox.isChecked():
            self.labelA.setStyleSheet('font-family: Lato; color: white; font-size: 15px')
            self.labelB.setStyleSheet('font-family: Lato; color: #9792E3; font-size: 15px')
        else: 
            self.labelA.setStyleSheet('font-family: Lato; color: #9792E3;; font-size: 15px')
            self.labelB.setStyleSheet('font-family: Lato; color: white; font-size: 15px')

    def setupUI(self, initial_state, optionA, optionB):
        self.setSpacing(10)
        self.addStretch()
        self.labelA = QLabel(str(optionA))
        self.labelB = QLabel(str(optionB))
        self.addWidget(self.labelA)
        self.checkbox = AnimatedSwitch(initial_state=initial_state)
        self.addWidget(self.checkbox)
        self.addWidget(self.labelB)
        self.addStretch()
        self.toggleBoldText()
        self.checkbox.toggled.connect(self.toggleBoldText)


    def text(self):
        if self.checkbox.isChecked():
            return self._optionB
        return self._optionA

# Info Page
class Info(QWidget):
    def __init__(self):
        super().__init__()
        # Run setup
        self.setupUI()
    
    def setupUI(self):
        # Variables
        layout = QVBoxLayout()
        self.filing_status = AnimatedSwitchBox('Single', 'Married', True)
        self.dependents = LabeledText('0', 'Dependents', 'NOT CURRENTLY FUNCTIONAL')

        layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        layout.addSpacing(50)
        layout.addLayout(self.filing_status)
        layout.addSpacing(25)
        layout.addLayout(self.dependents)
        layout.addStretch(1)
        self.setLayout(layout)

    def save(self):
        married = False if self.filing_status.text() == 'Single' else True
        upd = {
            'self.married' : married
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
        self.wages.setToolTip('(Box 1; 401(k), Simple IRA, 403(b) annuity, or 457 government already subtracted)')
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

    def save(self):
        upd = {
            'self.wages' : float(self.wages.text()),
            'self.fed_tax_witheld' : float(self.fed_tax_witheld.text()),
            'self.st_tax_witheld' : float(self.st_tax_witheld.text()),
            'self.int_income' : float(self.int_field.text()),
            'self.div_ordinary' : float(self.div_field.text()),
            'self.div_qualified' : float(self.div2_field.text()),
            'self.short_gains' : float(self.short_field.text()),
            'self.long_gains' : float(self.long_field.text()),
            'self.cap_distributions' : float(self.distributions.text()),
            'self.nec_total' : float(self.nec_field.text()),
            'self.unemployment_income' : float(self.unemploy_field.text())
        }
        Calculator.Calculator.updateFields(upd)

class Deductions(QScrollArea):
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
        self.deduction_type = AnimatedSwitchBox('Standard Deduction', 'Itemized Deduction', True)
        self.std_deduction = LabeledText('25900', 'Current Standard Deduction')
        self.charity = LabeledText('0', 'Charitable Contributions')
        self.ga_deduction = LabeledText('4600', 'GA Standard Deduction')
        self.ga_exemption = LabeledText('2700', 'GA Exemption')
        title1 = QLabel('Standard Deduction:')
        title2 = QLabel('Itemized Deduction')
        self.medical_dental = LabeledText('0', 'Medical and Dental Expenses', '(e.g. Prescriptions, Doctor visits, X-Rays, Glasses, Contacts + Saline solution)')
        self.state_local_tax = LabeledText('0', 'Paid State and Local Taxes', '(e.g. Previous year\'s state income tax or Sales tax paid throughout the year)')
        self.real_estate_tax = LabeledText('0', 'Real Estate Tax', '(e.g. County property taxes)')
        self.personal_prop_tax = LabeledText('0', 'Personal Property Tax', '(e.g Ad Valorem tax)')
        self.mortgage_interest = LabeledText('0', 'Paid Mortgage Interest (Form 1098)')
        self.pmi = LabeledText('0', 'Paid Mortgage Insurance Premiums')
        self.tithe = LabeledText('0', 'Tithe')
        self.donated_items = LabeledText('0', 'Fair Price of Donated Items')
        self.gambling_loss = LabeledText('0', 'Gambling Losses')
        
        title1.setAlignment(Qt.AlignmentFlag.AlignLeft)
        title2.setAlignment(Qt.AlignmentFlag.AlignLeft)

        layout.addSpacing(50)
        layout.addLayout(self.deduction_type)
        layout.addSpacing(25)
        layout.addWidget(title1)
        layout.addLayout(self.std_deduction)
        layout.addSpacing(25)
        layout.addLayout(self.charity)
        layout.addSpacing(25)
        layout.addLayout(self.ga_deduction)
        layout.addSpacing(25)
        layout.addLayout(self.ga_exemption)
        layout.addSpacing(25)
        layout.addWidget(title2)
        layout.addSpacing(25)
        layout.addLayout(self.medical_dental)
        layout.addSpacing(25)
        layout.addLayout(self.state_local_tax)
        layout.addSpacing(25)
        layout.addLayout(self.real_estate_tax)
        layout.addSpacing(25)
        layout.addLayout(self.personal_prop_tax)
        layout.addSpacing(25)
        layout.addLayout(self.mortgage_interest)
        layout.addSpacing(25)
        layout.addLayout(self.pmi)
        layout.addSpacing(25)
        layout.addLayout(self.tithe)
        layout.addSpacing(25)
        layout.addLayout(self.donated_items)
        layout.addSpacing(25)
        layout.addLayout(self.gambling_loss)
        layout.addStretch(1)

        # Contain layout in widget
        self.setWidget(container)
        

    def save(self):
        # Add line that sets a variable to check if using standard deduction or not
        itemizing = False if self.deduction_type.text() == 'Standard Deduction' else True
        upd = {
            'self.ITEMIZING' : itemizing,
            'self.STD_DEDUCTION' : float(self.std_deduction.text()),
            'self.GA_DEDUCTION' : float(self.ga_deduction.text()),
            'self.GA_EXEMPT' : float(self.ga_exemption.text()),
            'self.medical_dental' : float(self.medical_dental.text()),
            'self.state_local_tax' : float(self.state_local_tax.text()),
            'self.real_estate_tax' : float(self.real_estate_tax.text()),
            'self.personal_prop_tax' : float(self.personal_prop_tax.text()),
            'self.mortgage_interest' : float(self.mortgage_interest.text()),
            'self.pmi' : float(self.pmi.text()),
            'self.tithe' : float(self.tithe.text()),
            'self.donated_items' : float(self.donated_items.text()),
            'self.gambling_loss' : float(self.gambling_loss.text())
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
        self.meal_expense = LabeledText('0', 'Meal Expenses (for Self-Employed)')
        
        my_sizer.addSpacing(50)
        my_sizer.addLayout(self.education_credit)
        my_sizer.addSpacing(50)
        my_sizer.addLayout(self.recovery_credit)
        my_sizer.addSpacing(50)
        my_sizer.addLayout(self.meal_expense)
        my_sizer.addStretch(1)

        self.setLayout(my_sizer)

    def save(self):
        upd = {
            'self.edu_expenses' : float(self.education_credit.text()),
            'self.stimulus_credit' : float(self.recovery_credit.text()),
            'self.meal_expense' : float(self.meal_expense.text())
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
        sep.setStyleSheet('color: #847DDE;')

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
        calc.fillSchC()
        calc.fillSE()
        calc.fillSch1()
        calc.fillSch2()
        calc.fillSchD()
        calc.calcAdjIncome()
        calc.fillSchA()
        calc.fill8995()
        calc.adjustTax()
        calc.fillCapGain()
        calc.calcStateTax()
        calc.fill8863()
        calc.fillSch3()
        calc.fill1040()
        calc.fillState()
        calc.calcEstPayments()
        res = calc.getFields()
        grand_total = int(res['self.refund_owe_total'] + res['self.st_refund_owe_total'])
        # Set text values and colors. 
        self.fed_total.setText(f'<h1>${str(abs(int(res["self.refund_owe_total"])))}</h1>')
        self.st_total.setText(f'<h1>${str(abs(int(res["self.st_refund_owe_total"])))}</h1>')
        self.total.setText(f'<h1>${str(abs(grand_total))}</h1>')
        if (res['self.req_payments'] == True):
            self.monthly.setText(f'<h2>Yes, ${str(int(res["self.est_payments"]))}</h2>')
            self.monthly.setStyleSheet('color: #DB5461')
        else:
            self.monthly.setText(f'<h2>No! Estimate is ${str(int(res["self.est_payments"]))}</h2>')
            self.monthly.setStyleSheet('color: #ACE894')
        if res['self.refund_owe_total'] < 0:
            self.fed_total.setStyleSheet('color: #DB5461')
        else:
            self.fed_total.setStyleSheet('color: #ACE894')
        if res['self.st_refund_owe_total'] < 0:
            self.st_total.setStyleSheet('color: #DB5461')
        else:
            self.st_total.setStyleSheet('color: #ACE894')
        if grand_total < 0:
            self.total.setStyleSheet('color: #DB5461')
        else:
            self.total.setStyleSheet('color: #ACE894')

def load_fonts_from_dir(directory):
    families = set()
    for fi in QDir(directory).entryInfoList(['*.ttf']):
        _id = QFontDatabase.addApplicationFont(fi.absoluteFilePath())
        families |= set(QFontDatabase.applicationFontFamilies(_id))
    return families

# Main method
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet("""
        #toolsContainer { background-color: #1B1F23;}
        #toolsContainer QWidget { background-color: #1B1F23;}
        #toolsContainer QPushButton { background-image: url('exit24.png'); border: none; width: 24px; height: 24px;}
        #toolsContainer QPushButton:hover { background-color: #47525C; }
        #toolsContainer QPushButton:pressed { background-color: #505C68;}

        #tabContainer { background-color: #23292E;}
        #tabContainer QWidget { background-color: #23292E;}
        #tabContainer QPushButton { background-color: #23292E; color: white; border: none; padding: 3px; height: 50%;}
        #tabContainer QPushButton:hover { background-color: #47525C; }
        #tabContainer QPushButton:pressed { background-color: #9792E3;}
        #tabContainer QPushButton:disabled { background-color: #373F47; border-left-style: inset; border-left-width: 5px; border-left-color: #847DDE;}

        QWidget {background-color: #373F47; color: white;}
        QLabel {font-family: Lato; font-size: 15px;} 
        QLineEdit {
            background-color: #21252B;
            border-radius: 5px;
            border: 2px solid #21252B;
            padding-left: 10px;
            selection-color: rgb(255, 255, 255);
            selection-background-color: rgb(255, 121, 198);
            font-size: 15px;
        }
        QLineEdit:hover {
            border: 2px solid rgb(64, 71, 88);
        }
        QLineEdit:focus {
            border: 2px solid rgb(91, 101, 124);
        }

        QPushButton { border: none; background-color: #23292E; }
        QPushButton:hover { background-color: #47525C; }
        QPushButton:pressed { background-color: #9792E3; }
        QScrollBar:vertical { width:15px; background: #373F47; border:none } 
        QScrollBar::handle:vertical { background-color: #847DDE; }
        QScrollBar::handle:vertical:hover { background-color: #9792E3; }
        QScrollBar::sub-line:vertical, QScrollBar::add-line:vertical { background:none; }
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background:none; }

""")
    font_dir = './fonts'
    families = load_fonts_from_dir(os.fspath(font_dir))
    styles = QFontDatabase.styles('Lato')
    tg = TaxGui()
    tg.resize(900,700)
    tg.show()
    app.exec()
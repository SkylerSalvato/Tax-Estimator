import sys

class Calculator:
    PCT_SE = 0.9235 # Percent of wages taxed by Self Employment Tax (FICA)
    TAX_SE = 0.029 # Self Employment Tax
    PCT_AOC = 0.25
    PCT_AOC_REFUND = 0.4
    MAX_EDUCATORS_EXPENSE = 250
    values = {
        # State and federal return variables
        "self.wages" : 0,
        "self.adjusted_gross_income" : 0,
        "self.ITEMIZING" : False,
        "self.TOT_ITEMIZED" : 0,
        "self.STD_DEDUCTION" : 25900,
        "self.GA_DEDUCTION" : 4600,
        "self.GA_EXEMPT" : 2700,
        "self.taxable_income" : 0,
        "self.st_taxable_income" : 0,
        "self.tax" : 0,
        "self.st_tax" : 0,
        "self.total_tax" : 0,
        "self.fed_tax_witheld" : 0,
        "self.st_tax_witheld" : 0,
        "self.stimulus_credit" : 0,
        "self.refundable_credit" : 0,
        "self.total_payments" : 0,
        "self.refund_owe_total" : 0,
        "self.refund" : False,
        "self.married" : True,
        "self.charitable_contributions": 0, # Max 600 (married)

        # 1099-NEC & 1099-G variables
        "self.nec_total" : 0,
        # self.nec_tax_witheld : 0,
        "self.unemployment_income" : 0,
        "self.business_deduction" : 0,

        # 1099-self.& 1099-DIV & 1099-B variables
        # self.num_int : 0,
        "self.int_income" : 0,
        "self.cap_distributions" : 0,
        "self.div_ordinary" : 0,
        "self.div_qualified" : 0,
        "self.short_gains" : 0,
        "self.long_gains" : 0,
        "self.net_long_gains" : 0,
        "self.cap_gains" : 0,

        # Schedule 1 variables
        "self.other_income" : 0,
        "self.adjust_income" : 0,
        "self.gambling_income" : 0,
        "self.stock_options" : 0,
        "self.rental_income" : 0,
        "self.educator_expenses" : 0,
        "self.hsa_contributions" : 0,
        "self.student_loan_interest" : 0,
        "self.rental_expenses" : 0,

        # Schedule 2 variables
        "self.se_tax" : 0,

        # Schedule 3 variables #Not needed at the moment
        #self.dependent_child
        #self.retirement_contr_credit
        #self.energy_credit
        "self.nonrefundable_credits" : 0,

        # Schedule A (Itemized Deductions)
        "self.medical_dental" : 0,
        "self.state_local_tax" : 0,
        "self.real_estate_tax" : 0,
        "self.personal_prop_tax" : 0,
        "self.mortgage_interest" : 0,
        "self.pmi" : 0,
        "self.tithe" : 0,
        "self.donated_items" : 0,
        "self.gambling_loss" : 0,

        # Schedule C
        "self.meal_expense" : 0,

        # Schedule SE variables
        "self.fica_tax" : 0,
        "self.half_fica_tax" : 0,

        # 8863 variables
        "self.edu_expenses" : 0,
        "self.aoc_credit" : 0,
        "self.refundable_aoc" : 0,
        "self.nonrefundable_aoc" : 0,

        # Estimated taxes
        "self.est_payments" : 0,
        "self.req_payments" : False,
        "self.est_tax" : 0
        }

    def __init__(self):
        self.fed_brackets_single = [
            [0.00, 9875.00, 0.10, 0], # min (excl), max (incl), tax rate, sum of prev.
            [9875.00, 40125.00, 0.12, 987.50],
            [40125.00, 85525.00, 0.22, 4617.50],
            [85525.00, 163300.00, 0.24, 14605.50],
            [163300.00, 207350.00, 0.32, 33271.50],
            [207350.00, 518400.00, 0.35, 47367.50],
            [518400.00, sys.float_info.max, 0.37, 156235.00]
        ]
        self.fed_brackets_married = [
            [0.00, 20550.00, 0.10, 0],
            [20550.00, 83550.00, 0.12, 8503.00],
            [83550.00, 178150.00, 0.22, 11958.00],
            [178150.00, 340100.00, 0.24, 38346.00],
            [340100.00, 431900.00, 0.32, 50911.50],
            [431900.00, 647850.00, 0.35, 50911.50],
            [647850.00, sys.float_info.max, 0.37, 63477.50]
        ]
        self.st_brackets_single = [
            [0.00, 750.00, 0.01, 0],
            [750.00, 2250.00, 0.02, 8.00],
            [2250.00, 3750.00, 0.03, 38.00],
            [3750.00, 5250.00, 0.04, 83.00],
            [5250.00, 7000.00, 0.05, 143.00],
            [7000.00, sys.float_info.max, 0.0575, 230.00]
        ]
        self.st_brackets_married = [
            [0.00, 1000.00, 0.01, 0],
            [1000.00, 3000.00, 0.02, 10.00],
            [3000.00, 5000.00, 0.03, 50.00],
            [5000.00, 7000.00, 0.04, 110.00],
            [7000.00, 10000.00, 0.05, 190.00],
            [10000.00, sys.float_info.max, 0.0575, 340.00]
        ]

    def fillSE(self):
        six = self.values["self.net_business_profit"] * Calculator.PCT_SE
        ten = six * 0.124
        eleven = six * Calculator.TAX_SE
        self.values["self.fica_tax"] = ten + eleven
        self.values["self.half_fica_tax"] = self.values["self.fica_tax"] * 0.5

    def fillSch1(self):
        self.values["self.other_income"] = self.values["self.net_business_profit"] + self.values["self.unemployment_income"]
        self.values["self.other_income"] += self.values["self.gambling_income"]
        self.values["self.other_income"] += self.values["self.stock_options"]
        self.values["self.other_income"] += self.values["self.rental_income"]

        self.values["self.adjust_income"] = self.values["self.half_fica_tax"]
        self.values["self.adjust_income"] += min(Calculator.MAX_EDUCATORS_EXPENSE, self.values["self.educator_expenses"])
        self.values["self.adjust_income"] += self.values["self.hsa_contributions"]
        self.values["self.adjust_income"] += self.values["self.rental_expenses"]
        temp_total_income = self.values["self.int_income"] + self.values["self.div_ordinary"] + self.values["self.cap_gains"] + self.values["self.wages"] + self.values["self.other_income"]
        temp_adjusted_gross_income = temp_total_income - self.values["self.adjust_income"]
        student_loan_int_max = temp_adjusted_gross_income - 70000 if not self.values["self.married"] else temp_adjusted_gross_income - 140000
        student_loan_int_percent = round(student_loan_int_max / 15000, 3) if not self.values["self.married"] else round(student_loan_int_max / 30000, 3)
        tot_student_loan_int_deduction = min(2500, self.values["self.student_loan_interest"]) * student_loan_int_percent
        self.values["self.adjust_income"] += tot_student_loan_int_deduction
  
    def fillSch2(self):
        self.values["self.se_tax"] = self.values["self.fica_tax"]
  
    def fillSch3(self):
        self.values["self.nonrefundable_credits"] = self.values["self.nonrefundable_aoc"]

    def fillSchA(self):
        ### Medical and Dental Expenses (exceeding 7.5% Adjusted Gross Income)
        # Premiums (unless paid with pre-tax dollars)
        # Prescriptions
        # Doctor visits
        # Exams, Labs, Tests
        # Glasses, Conacts (+ Saline solution and Enzyme cleaner), LASIK
        # Ambulance, or yourself
        # Breast pumps
        med_dent = max(0, self.values["self.medical_dental"] - self.values["self.adjusted_gross_income"] * 7.5)
        
        ### Taxes You Paid
        # State and local income tax (or Sales tax but that requires tracking everything you buy, but good if you buy a car or keep track of everything)
        # Property (Real Estate) taxes
        # Personal Property taxes (Car Registration) 
        tax_you_paid = min(5000, self.values["self.state_local_tax"] + self.values["self.real_estate_tax"] + self.values["self.personal_prop_tax"]) if not self.values["self.married"] else min(10000, self.values["self.state_local_tax"] + self.values["self.real_estate_tax"] + self.values["self.personal_prop_tax"]) 

        ### Interest You Paid
        # Mortgage Interest 
        # Mortgage Insurance Premiums (max Adjusted Gross Income = 109000)
        # (Student Loan Interest goes to Sch 1) 
        interest_you_paid = self.values["self.mortgage_interest"] + self.values["self.pmi"] if self.values["self.adjusted_gross_income"] <= 100000 else self.values["self.mortgage_interest"]

        ### Gifts to Charity
        # Tithe 
        # Donated Used Items
        gifts = self.values["self.tithe"] + self.values["self.donated_items"]

        ### Casualty and Theft Losses

        ### Other Itemized Deductions
        # Gambling Losses
        other = self.values["self.gambling_loss"]

        ### Total
        self.values["self.TOT_ITEMIZED"] = med_dent + tax_you_paid + interest_you_paid + gifts + other
        pass

    def fillSchC(self):
        gross = self.values["self.nec_total"]
        total_expenses = (self.values["self.meal_expense"] * 0.5)
        self.values["self.net_business_profit"] = gross - total_expenses

    def fillSchD(self):
        self.values["self.net_long_gains"] = self.values["self.long_gains"] + self.values["self.cap_distributions"]
        self.values["self.cap_gains"] = self.values["self.net_long_gains"] + self.values["self.short_gains"]

    def adjustTax(self):
        if self.values["self.ITEMIZING"]:
            deductions = [
                self.values["self.TOT_ITEMIZED"],
                self.values["self.business_deduction"]
            ]
        else:
            deductions = [
                self.values["self.STD_DEDUCTION"] if not self.values["self.married"] else 2.00 * self.values["self.STD_DEDUCTION"],
                self.values["self.charitable_contributions"],
                self.values["self.business_deduction"]
            ]
        st_deductions = [
            self.values["self.GA_DEDUCTION"],
            self.values["self.GA_EXEMPT"]
        ]
        self.values["self.taxable_income"] = Calculator.massDeduct(self.values["self.adjusted_gross_income"], deductions)
        self.values["self.st_taxable_income"] = Calculator.massDeduct(self.values["self.adjusted_gross_income"], st_deductions)

    def fillCapGain(self):
        # 1. get 1040 line 15 (taxable income)
        one = self.values["self.taxable_income"]
        # 2. get 1040 line 3a (qualified dividends)
        # 3. get 1040 line 7 (capital gain or loss)
        # 4. add 2 and 3
        three = min(self.values["self.net_long_gains"], self.values["self.cap_gains"])
        four = self.values["self.div_qualified"] + three
        # 5. subtract 4 from 1
        five = max(0, one - four)
        # 6. enter 40,400 if single or 80,800 if married
        # 7. min(line 1, line 6)
        seven = min(one, 40400) if not self.values["self.married"] else min(one, 80800)
        # 8. min(line 5, line 7)
        eight = min(five, seven)
        # 9. subtract 8 from 7 (taxed at 0%)
        nine = seven - eight
        # 10. min(line 1, line 4)
        ten = min(one, four)
        # 11. line 9
        # 12. subtract 11 from 10
        twelve = ten - nine
        # 13. enter 445,850 if single or 501600 if married
        # 14. min(line 1, line 13)
        fourteen = min(one, 445,850) if not self.values["self.married"] else min(one, 501600)
        # 15. add 5 to 9
        fifteen = five + nine
        # 16. subtract 15 from 14 (min value is 0)
        sixteen = max(fourteen - fifteen, 0)
        # 17. min(line 12, line 16)
        # 18. 17 taxed at 15% (17 x 0.15)
        eighteen = min(twelve, sixteen) * 0.15
        # 19. add 9 to 17
        # 20. subtract 19 from 10
        # 21. 20 taxed at 20%
        twentyone = (ten - (nine + min(twelve, sixteen))) * 0.2
        # 22. use tax computation worksheet to figure tax on line 5
        twentytwo = Calculator.calcSimpleTax(self.fed_brackets_single, five) if not self.values["self.married"] else Calculator.calcSimpleTax(self.fed_brackets_married, five)
        # 23. add 18, 21, and 22
        twentythree = eighteen + twentyone + twentytwo
        # 24. use tax computation worksheet to figure tax on line 1
        twentyfour = Calculator.calcSimpleTax(self.fed_brackets_single, one) if not self.values["self.married"] else Calculator.calcSimpleTax(self.fed_brackets_married, one)
        # 25. min(line 23, line 24) -> send to 1040 line 16 blank space with checkbox
        self.values["self.tax"] = min(twentythree, twentyfour)

    def calcAdjIncome(self):
        total_income = self.values["self.int_income"] + self.values["self.div_ordinary"] + self.values["self.cap_gains"] + self.values["self.wages"] + self.values["self.other_income"]
        self.values["self.adjusted_gross_income"] = total_income - self.values["self.adjust_income"]
  
    def calcFedTax(self):
        if not self.values["self.married"]:
            return Calculator.calcSimpleTax(self.fed_brackets_single, self.values["self.taxable_income"])
        else:
            return Calculator.calcSimpleTax(self.fed_brackets_married, self.values["self.taxable_income"])
    
    def calcStateTax(self):
        if not self.values["self.married"]:
            self.values["self.st_tax"] = Calculator.calcSimpleTax(self.st_brackets_single, self.values["self.st_taxable_income"])
        else:
            self.values["self.st_tax"] = Calculator.calcSimpleTax(self.st_brackets_married, self.values["self.st_taxable_income"])

    def fill8863(self):
        tweight = self.values["self.edu_expenses"] - 2000.00 # (1/4 for amt above 2000)
        twnine = tweight * Calculator.PCT_AOC
        if (tweight <= 0):
            self.values["self.aoc_credit"] = self.values["self.edu_expenses"]
        else:
            self.values["self.aoc_credit"] = 2000.00 + twnine
    
        self.values["self.refundable_aoc"] = Calculator.PCT_AOC_REFUND * self.values["self.aoc_credit"]
        nine = self.values["self.aoc_credit"] - self.values["self.refundable_aoc"]
        self.values["self.nonrefundable_aoc"] = min(nine, self.values["self.tax"])

    def fill8995(self):
        five = (self.values["self.nec_total"] - self.values["self.half_fica_tax"]) * 0.2
        if self.values["self.ITEMIZING"]:
            deductions = [
                self.values["self.TOT_ITEMIZED"]
            ]
        else:
            deductions = [
                self.values["self.STD_DEDUCTION"] if not self.values["self.married"] else 2.00 * self.values["self.STD_DEDUCTION"], 
                self.values["self.charitable_contributions"]
            ]
        precalculated = Calculator.massDeduct(self.values["self.adjusted_gross_income"], deductions)
        fourteen = (precalculated - self.values["self.cap_gains"]) * 0.2
        self.values["self.business_deduction"] = max(0, min(five, fourteen))

    def fill1040(self):
        self.values["self.total_tax"] = max(0, (self.values["self.tax"] - self.values["self.nonrefundable_credits"])) # Line 22
        self.values["self.total_tax"] += self.values["self.se_tax"] # Line 24
        self.values["self.refundable_credit"] = (self.values["self.refundable_aoc"] + self.values["self.stimulus_credit"])
        self.values["self.total_payments"] = (self.values["self.fed_tax_witheld"] + self.values["self.refundable_credit"])
        self.values["self.refund_owe_total"] = (self.values["self.total_payments"] - self.values["self.total_tax"])

    def fillState(self):
        self.values["self.st_refund_owe_total"] = self.values["self.st_tax_witheld"] - self.values["self.st_tax"]

    def calcEstPayments(self):
        self.values["self.est_tax"] = max(0, self.values["self.total_tax"] - self.values["self.refundable_credit"])
        twelve = self.values["self.est_tax"] * 0.9
        fourteen = (twelve - self.values["self.fed_tax_witheld"]) <= 0
        if not fourteen:
            self.values["self.req_payments"] = (self.values["self.est_tax"] - self.values["self.fed_tax_witheld"]) > 1000  
        self.values["self.est_payments"] = max(0, (self.values["self.est_tax"] - self.values["self.fed_tax_witheld"]) * 0.25)

    @staticmethod
    def calcSimpleTax(taxTable, taxableIncome):
        for bracket in taxTable:
            if (taxableIncome > bracket[0] and taxableIncome <= bracket[1]):
                    return bracket[3] + bracket[2] * (taxableIncome - bracket[0])
        return 0
    
    @staticmethod
    def massDeduct(value, deductions):
        for d in deductions:
            value -= d
        return value

    @staticmethod
    def updateFields(dictOfValues):
        for key in dictOfValues:
            if key in Calculator.values:
                Calculator.values[key] = dictOfValues[key]
  
    def getFields(self):
        return self.values
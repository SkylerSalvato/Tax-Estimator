import sys

class Calculator:
    PCT_SE = 0.9235 # Percent of wages taxed by Self Employment Tax (FICA)
    TAX_SE = 0.029 # Self Employment Tax
    PCT_AOC = 0.25
    PCT_AOC_REFUND = 0.4
    values = {
        # State and federal return variables
        "self.wages" : 0,
        "self.adjusted_gross_income" : 0,
        "self.STD_DEDUCTION" : 12550,
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
        "self.married" : False,

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

        # Schedule 2 variables
        "self.se_tax" : 0,

        #Schedule 3 variables #Not needed at the moment
        #self.dependent_child
        #self.retirement_contr_credit
        #self.energy_credit
        

        # Schedule SE variables
        "self.fica_tax" : 0,
        "self.half_fica_tax" : 0,

        # 8863 variables
        "self.edu_expenses" : 0,
        "self.aoc_credit" : 0,
        "self.refundable_aoc" : 0,
        "self.nonrefundable_aoc" : 0
        }

    def __init__(self):
        self.fed_brackets = [
            [0.00, 9875.00, 0.10, 0], # min (excl), max (incl), tax rate, sum of prev.
            [9875.00, 40125.00, 0.12, 987.50],
            [40125.00, 85525.00, 0.22, 4617.50],
            [85525.00, 163300.00, 0.24, 14605.50],
            [163300.00, 207350.00, 0.32, 33271.50],
            [207350.00, 518400.00, 0.35, 47367.50],
            [518400.00, sys.float_info.max, 0.37, 156235.00]
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
        six = self.values["self.nec_total"] * Calculator.PCT_SE
        ten = six * 0.124
        eleven = six * Calculator.TAX_SE
        self.values["self.fica_tax"] = ten + eleven
        self.values["self.half_fica_tax"] = self.values["self.fica_tax"] * 0.5

    def fillSch1(self):
        self.values["self.other_income"] = self.values["self.nec_total"] + self.values["self.unemployment_income"]
        self.values["self.adjust_income"] = self.values["self.half_fica_tax"]
  
    def fillSch2(self):
        self.values["self.se_tax"] = self.values["self.fica_tax"]
  
    def fillSch3(self):
        pass

    def fillSchD(self):
        self.values["self.net_long_gains"] = self.values["self.long_gains"] + self.values["self.cap_distributions"]
        self.values["self.cap_gains"] = self.values["self.net_long_gains"] + self.values["self.short_gains"]

    def adjustTax(self):
        self.values["self.taxable_income"] = (self.values["self.adjusted_gross_income"] - self.values["self.STD_DEDUCTION"] - self.values["self.business_deduction"]) if not self.values["self.married"] else (self.values["self.adjusted_gross_income"] - (2.00 * self.values["self.STD_DEDUCTION"]) - self.values["self.business_deduction"])
        three = self.values["self.net_long_gains"] if self.values["self.net_long_gains"] < self.values["self.cap_gains"] else self.values["self.cap_gains"]
        four = self.values["self.div_qualified"] + three
        five = (self.values["self.taxable_income"] - four) if (self.values["self.taxable_income"] - four) > 0 else 0
        six = 40000 if not self.values["self.married"] else 80000
        seven = self.values["self.taxable_income"] if self.values["self.taxable_income"] < six else six
        eight = five if five < seven else seven
        nine = seven - eight # Taxed at 0%
        ten = four if four < self.values["self.taxable_income"] else self.values["self.taxable_income"]
        twentyfour = self.calcFedTax()
        hold = self.values["self.taxable_income"]
        self.values["self.taxable_income"] = five
        twentytwo = self.calcFedTax()
        self.values["self.tax"] = twentytwo if twentytwo < twentyfour else twentyfour
        self.values["self.taxable_income"] = hold

    def calcAdjIncome(self):
        total_income = self.values["self.int_income"] + self.values["self.div_ordinary"] + self.values["self.cap_gains"] + self.values["self.wages"] + self.values["self.other_income"]
        self.values["self.adjusted_gross_income"] = total_income - self.values["self.adjust_income"]
  
    def calcFedTax(self):
        if (not self.values["self.married"]):
            for i in range(len(self.fed_brackets)): 
                if (self.values["self.taxable_income"] > self.fed_brackets[i][0] and self.values["self.taxable_income"] <= self.fed_brackets[i][1]):
                    return self.fed_brackets[i][3] + self.fed_brackets[i][2] * (self.values["self.taxable_income"] - self.fed_brackets[i][0])
                return 0
        else:
            for i in range(len(self.fed_brackets)):
                if (self.values["self.taxable_income"] > (2.00 * self.fed_brackets[i][0]) and self.values["self.taxable_income"] <= (2.00 * self.fed_brackets[i][1])):
                    return (2.00 * self.fed_brackets[i][3]) + self.fed_brackets[i][2] * (self.values["self.taxable_income"] - (2.00 * self.fed_brackets[i][0]))
                return 0
    
    def calcStateTax(self):
        if (not self.values["self.married"]):
            self.values["self.st_taxable_income"] = self.values["self.adjusted_gross_income"] - (self.values["self.GA_DEDUCTION"] + self.values["self.GA_EXEMPT"])
            for i in range(len(self.st_brackets_single)):
                if (self.values["self.st_taxable_income"] > self.st_brackets_single[i][0] and self.values["self.st_taxable_income"] <= self.st_brackets_single[i][1]):
                    self.values["self.st_tax"] = self.st_brackets_single[i][3] + self.st_brackets_single[i][2] * (self.values["self.st_taxable_income"] - self.st_brackets_single[i][0])
        else:
            self.values["self.st_taxable_income"] = self.values["self.adjusted_gross_income"] - (self.values["self.GA_DEDUCTION"] + self.values["self.GA_EXEMPT"])
            for i in range(len(self.st_brackets_married)):
                if (self.values["self.st_taxable_income"] > self.st_brackets_married[i][0] and self.values["self.st_taxable_income"] <= self.st_brackets_married[i][1]):
                    self.values["self.st_tax"] = self.st_brackets_married[i][3] + self.st_brackets_married[i][2] * (self.values["self.st_taxable_income"] - self.st_brackets_married[i][0])

    def fill8863(self):
        tweight = self.values["self.edu_expenses"] - 2000.00 # (1/4 for amt above 2000)
        twnine = tweight * Calculator.PCT_AOC
        if (tweight <= 0):
            self.values["self.aoc_credit"] = self.values["self.edu_expenses"]
        else:
            self.values["self.aoc_credit"] = 2000.00 + twnine
    
        self.values["self.refundable_aoc"] = Calculator.PCT_AOC_REFUND * self.values["self.aoc_credit"]
        nine = self.values["self.aoc_credit"] - self.values["self.refundable_aoc"]
        if (nine < self.values["self.tax"]) :
            self.values["self.nonrefundable_aoc"] = nine
        else:
            self.values["self.nonrefundable_aoc"] = self.values["self.tax"]

    def fill8995(self):
        five = (self.values["self.nec_total"] - self.values["self.half_fica_tax"]) * 0.2
        precalculated = (self.values["self.adjusted_gross_income"] - self.values["self.STD_DEDUCTION"]) if not self.values["self.married"] else (self.values["self.adjusted_gross_income"] - (2.00 * self.values["self.STD_DEDUCTION"]))
        fourteen = (precalculated - self.values["self.cap_gains"]) * 0.2
        self.values["self.business_deduction"] = five if five < fourteen else fourteen
        if (self.values["self.business_deduction"] < 0):
            self.values["self.business_deduction"] = 0 

    def fill1040(self):
        if ((self.values["self.tax"] - self.values["self.nonrefundable_aoc"]) < 0):
            self.values["self.total_tax"] = 0
        else:
            self.values["self.total_tax"] = (self.values["self.tax"] - self.values["self.nonrefundable_aoc"]) # Line 22
    
        self.values["self.total_tax"] += self.values["self.se_tax"] # Line 24
        self.values["self.refundable_credit"] = (self.values["self.refundable_aoc"] + self.values["self.stimulus_credit"])
        self.values["self.total_payments"] = (self.values["self.fed_tax_witheld"] + self.values["self.refundable_credit"])
        self.values["self.refund_owe_total"] = (self.values["self.total_payments"] - self.values["self.total_tax"])

    def fillState(self):
        self.values["self.st_refund_owe_total"] = self.values["self.st_tax_witheld"] - self.values["self.st_tax"]

    @staticmethod
    def updateFields(dictOfValues):
        for key in dictOfValues:
            if key in Calculator.values:
                Calculator.values[key] = dictOfValues[key]
  
    def getFields(self):
        return self.values
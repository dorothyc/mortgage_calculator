"""
Code to perform mortgage calculations
"""
__author__ = "Dorothy Cheung"
__maintainer__ = "Dorothy Cheung"
__status__ = "Development"

class MortgageCalc:

    def __init__(self):
       self.interest_rate = 2.5

    def get_payment_amount(self, ask_price, down_pay, payment_schedule, amor_period):
      """Function to get payment amount depending on the input Params, it checks
        the amount to be borrowed (down_payment >= 5% for 1st 500k, 10% for rest, also atBor > down_pay) and
        amoritization period is within range (>= 5 <= 25)
                
            Params:
            ask_price  (str): Asking Price of the property
            down_pay (str): Must be at least 5% of first $500k plus 10% of any amount above $500k 
            payment_schedule (str): weekly, biweekly, monthly
            amor_period (str):  Min 5 years, max 25 years
          
            Return:
            float: payment amount round to 2 decimals
            -1 if it fails either amount borrow check or amoritization period check
      """ 
      ask_price = float(ask_price)
      down_pay = float(down_pay)
      amt_borrow = self.check_amt_bor(ask_price, down_pay)
      amor_period_pass = self.check_amor_period(amor_period)
      # check down_pay >= 5% for 1st 500k, 10% for rest, also atBor > down_pay
      if amt_borrow and amor_period_pass:
        insur_amt = self.calc_mort_insur(ask_price, down_pay)
        amt_bor = ask_price - down_pay + insur_amt
        annual_pay = self.calc_annual_pay(payment_schedule)
        period_interest = self.interest_rate/100/annual_pay
        discount_factor = self.calc_discount_factor(period_interest, annual_pay, amor_period)
        # round to 2 decimals
        return round(amt_bor/discount_factor, 2)
      else:
        return -1


    def get_mortgage_amount(self, payment_amount, payment_schedule, amor_period):
      """Function to calculate maximum mortgage that can be taken out depending on the payment
        amount, payment schedule and amoritization period (amount including paying insurance if applicable)

            Params:
            payment_amount (str): amount of periodic payment including insurance
            payment_schedule (str): weekly, biweekly, monthly
            amor_period (str):  Min 5 years, max 25 years
          
            Return:
            float: maximum mortage round to 2 decimals
            -1 if the function results in divided by zero error
      """ 
      amor_period_pass = self.check_amor_period(amor_period) 
      # Check range of amor_period: 5 yrs to 25 yrs
      if amor_period_pass:
        payment_amount = float(payment_amount)
        annual_pay = self.calc_annual_pay(payment_schedule)
        period_interest = self.interest_rate/100/annual_pay
        discount_factor = self.calc_discount_factor(period_interest, annual_pay, amor_period)
        if discount_factor != -1:
          # round to 2 decimals
          return round(payment_amount * discount_factor, 2)
        else:
          return -1
      return -1


    def patch_int_rate(self, rate):
      """Function to change the interest rate; this function does not check the rate number itself 

            Params:
            rate (str): interest rate to be updated

            Return:
            list[]: old rate, new rate
      """ 
      try:
        old_rate = self.interest_rate
        self.interest_rate = float(rate)
        return [old_rate, self.interest_rate]
      except ValueError as err:
        print ("Error:", err)
        return -1


    def calc_discount_factor(self, period_interest, annual_pay, amor_period):
      """Function to calculate the discount factor which is used by get_payment_amount and get_mortage_amount functions

            Params: 
            period_interest (str): Number of Periodic Payments (n) = Payments per year times number of years
            annual_pay (str): Periodic Interest Rate, annual rate divided by number of payments per year
            amor_period (str):  Min 5 years, max 25 years
          
            Return:
            float: discount factor 
            -1 if the function results in divided by zero error
      """ 
      # Number of Periodic Payments (n) = Payments per year times number of years
      period_interest = float(period_interest)
      annual_pay = int(annual_pay)
      amor_period = int(amor_period)
      # Periodic Interest Rate (i) = Annual rate divided by number of payments per year
      # D =  {[(1 + i) ^n] - 1} / [i(1 + i)^n]
      try:
        return (((1+period_interest)**(annual_pay*amor_period))-1) / (period_interest*(1+period_interest)**(annual_pay*amor_period))
      except ZeroDivisionError as err:
        print ("Error:", err)
        return -1


    def calc_annual_pay(self, payment_schedule):
      """Function to translate the payment schedule string to an integer

            Params:
            payment_schedule (str): weekly, biweekly, monthly
           
            Return:
            float: integer of 12, 26, 52 depending on the payment_schedule input
            -1 if payment_schedule not equal to one of weekly, biweekly, monthly
      """ 
      # check payment_schedule: weekly (52), biweekly (26), monthly (12)
      try:
        if payment_schedule == 'monthly':
            annual_pay = 12
        elif payment_schedule == 'biweekly':
            annual_pay = 26
        elif payment_schedule == 'weekly':
            annual_pay = 52
      except ValueError:
        annual_pay = -1
      return annual_pay


    def check_amt_bor(self, ask_price, down_pay):
      """Function to check whether the down payment is enough for the amount to be borrowed
        Note that ask_price must be > down_pay

            Params:
            ask_price  (str): Asking Price of the property
            down_pay (str): Must be at least 5% of first $500k plus 10% of any amount above $500k 
          
            Return:
            bool: True if down_pay is larger than requirement; False if otherwise
      """ 
      # check down_pay >= 5% for 1st 500k, 10% for rest, also amount_Bor > down_pay
      ask_price = float(ask_price)
      down_pay = float(down_pay)
      if ask_price > down_pay:
        if ask_price <= 500000:
          amt_bor_ok = (down_pay >= ask_price * 0.05)
        else:
          amt_bor_ok = (down_pay >= ((ask_price-500000)*0.1 + 25000))
      else:
        amt_bor_ok = False
      return amt_bor_ok


    def check_amor_period(self, amor_period):
      """Function to check whether the amoritization period is within range defined

            Params: 
            amor_period (str):  Min 5 years, max 25 years
          
            Return:
            bool: True if within range; False otherwise
      """ 
      # Check range of amor_period: 5 yrs to 25 yrs
      amor_period = int(amor_period)
      if amor_period < 5 or amor_period > 25:
        amor_period_ok = False
      else:
        amor_period_ok = True
      return amor_period_ok


    def calc_mort_insur(self, ask_price, down_pay):
      """Function to calculate the mortage insurance depending on asking price and down payment 
        (insurance based mortage amount)

            Params:
            ask_price  (str): Asking Price of the property
            down_pay (str): Must be at least 5% of first $500k plus 10% of any amount above $500k 
          
            Return:
            float: insurance amount to be paid as part of the mortage, Return 0 if mortage amount > 1 million
            or less than 5% down payment (when < 1 mil)
      """ 
      # flags an error when mortages > 1mil
      # add if down_pay < 20% of ask_price
      ask_price = float(ask_price)
      down_pay = float(down_pay)
      down_ratio = down_pay/ask_price*100
      mortage_amt = ask_price-down_pay
      # no insurance when mortages > 1million dollars
      if mortage_amt > 1000000:
        insur_amt = 0
        return insur_amt

      # check if down_ratio >= 5%
      if down_ratio >=5.0:
        if down_ratio < 10 and down_ratio >= 5.0:
          insur_amt = mortage_amt * 0.0315
        elif down_ratio < 15 and down_ratio >= 10:
          insur_amt = mortage_amt * 0.024
        elif down_ratio < 20 and down_ratio >= 15:
          insur_amt = mortage_amt * 0.018
        elif down_ratio >= 20:
          insur_amt = 0
      else:
        insur_amt = 0
      return insur_amt

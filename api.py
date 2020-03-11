"""
Code to run a Flask application
"""

from flask import Flask, request
import json, mortgage_calc

__author__ = "Dorothy Cheung"
__maintainer__ = "Dorothy Cheung"
__status__ = "Development"

# create a Flask instance
app = Flask(__name__)

# set Debug parameter to True to make changes without restarting the program
app.config["DEBUG"] = True

# create MortgageCalc instance
mc = mortgage_calc.MortgageCalc()

@app.route('/payment-amount', methods=['GET'])
def get_payment_amount():
    """Function to get payment amount depending on the input Params, it checks the amount to be borrowed (down_payment >= 5% for 1st 500k, 10% for rest, also atBor > down_pay) andamoritization period is within range (>= 5 <= 25)
            
        Params:
        asking_price  (str): Asking Price of the property
        down_payment (str): Must be at least 5% of first $500k plus 10% of any amount above $500k 
        payment_schedule (str): weekly, biweekly, monthly
        amor_period (str):  Min 5 years, max 25 years
        
        Return:
        json: payment amount round to 2 decimals
        json: payment if it fails either amount borrow check or amoritization period check
      """ 
    ask_price = request.args.get('asking_price')
    down_pay = request.args.get('down_payment')
    payment_schedule = request.args.get('payment_schedule')
    amor_period = request.args.get('amor_period')
    # check input
    if not ask_price or not down_pay or not payment_schedule or not amor_period:
        results = "check input"
        data = {"Error": results}
        response = app.response_class(response=json.dumps(data), status=400)
        return response

    # call function
    results = mc.get_payment_amount(ask_price, down_pay, payment_schedule, amor_period)

    # handle results
    if results != -1:
        data = {"payment_amount": results}
        response = app.response_class(response=json.dumps(data), status=200)
    else:
        results = "check down_pay >= 5% for 1st 500k, 10% for rest, also atBor > down_pay"
        data = {"Error": results}
        response = app.response_class(response=json.dumps(data), status=400)
    return response


@app.route('/mortgage-amount', methods=['GET'])
def get_mortage_amount():
    """Endpoint to get maximum mortgage that can be taken out depending on the payment amount, payment schedule and amoritization period (amount including paying insurance if applicable)

        Params:
        payment amount (str): amount of periodic payment including insurance
        payment_schedule (str): weekly, biweekly, monthly
        amor_period (str):  Min 5 years, max 25 years
        
        Return:
        json: maximum mortage round to 2 decimals
        json: if the function results in divided by zero error
    """  

    payment_amount = request.args.get('payment_amount')
    payment_schedule = request.args.get('payment_schedule')
    amor_period = request.args.get('amor_period')

    # check input
    if not payment_amount or not payment_schedule or not amor_period:
        results = "check input"
        data = {"Error": results}
        response = app.response_class(response=json.dumps(data), status=400)
        return response

    # call function
    results = mc.get_mortgage_amount(payment_amount, payment_schedule, amor_period)

    # handle results
    if results != -1:
        data = {"mortage_amount": results}
        response = app.response_class(response=json.dumps(data), status=200)
    else:
        results = "something went wrong. Check your input."
        data = {"Error": results}
        response = app.response_class(response=json.dumps(data), status=400)
    return response


@app.route('/interest-rate', methods=['PATCH'])
def update_interest_rate():
    """Function to change the interest rate; this function does not check the rate number itself 

        Params:
        json: interest rate to be updated

        Return:
        json: old rate, new rate
    """ 
    json_data = json.loads(request.data)
    
    # check input
    if not json_data:
        results = "check input"
        data = {"Error": results}
        response = app.response_class(response=json.dumps(data), status=400)
        return response

    # call function
    interest_rate = json_data['interest_rate']
    results = mc.patch_int_rate(interest_rate)

    # handle results
    if results != -1:
        # results returned format [old-interest-rate, new-interest-rate]
        data = {"old_interest_rate": results[0], "new_interest_rate": results[1]}
        response = app.response_class(response=json.dumps(data), status=200)
    else:
        results = "something went wrong. Check your input."
        data = {"Error": results}
        response = app.response_class(response=json.dumps(data), status=400)
    return response


if __name__ == "__main__":
    app.run()
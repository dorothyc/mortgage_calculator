"""
Code to run a Flask application
"""

import pytest
from flask import json
from api import app

__author__ = "Dorothy Cheung"
__maintainer__ = "Dorothy Cheung"
__status__ = "Development"

class TestMortgageCalc():

    def test_payment_amount_succeed(self): 
        """Test case where all parameters are correct and hence should succeed (status code 200)

            Params: (query string)
            asking_price  (str): Asking Price of the property
            down_payment (str): Must be at least 5% of first $500k plus 10% of any amount above $500k 
            payment_schedule (str): weekly, biweekly, monthly
            amor_period (str):  Min 5 years, max 25 years
          
            Return:
            json: status code 200
            json: payment amount, rounded to 2 decimals
        """ 
        response = app.test_client().get(
            '/payment-amount', 
            query_string="asking_price=50000&down_payment=20000&payment_schedule=monthly&amor_period=6"
        )
        data = json.loads(response.get_data(as_text=True))
        assert response.status_code == 200
        assert data['payment_amount'] == 449.13


    def test_payment_amount_fail(self):  
        """Test case where one of the parameters (amor_period) is missing and hence should fail (status code 400) with error message

            Params: (query string)
            asking_price  (str): Asking Price of the property
            down_payment (str): Must be at least 5% of first $500k plus 10% of any amount above $500k 
            payment_schedule (str): weekly, biweekly, monthly
          
            Return:
            json: status code 400, error message
        """      
        response = app.test_client().get(
            '/payment-amount', 
            query_string="asking_price=50000&down_payment=10000&payment_schedule=monthly"
        )
        data = json.loads(response.get_data(as_text=True))
        assert response.status_code == 400
        assert data['Error'] == "check input"


    def test_mortgage_amount_succeed(self): 
        """Test case where all parameters are correct and hence should succeed (status code 200)

            Params:
            payment_amount (str): amount of periodic payment including insurance
            payment_schedule (str): weekly, biweekly, monthly
            amor_period (str):  Min 5 years, max 25 years
          
            Return:
            json: status code 200, maximum mortage amount (rounded to 2 decimals)
        """ 
        response = app.test_client().get(
            '/mortgage-amount', 
            query_string="payment_amount=449.13&payment_schedule=monthly&amor_period=6"
        )
        data = json.loads(response.get_data(as_text=True))
        assert response.status_code == 200
        assert data['mortage_amount'] == 29999.95

    def test_mortgage_amount_fail(self): 
        """Test case where one of the parameters (amor_period) is wrong and hence should fail (status code 400) with error message

            Params:
            payment_amount (str): amount of periodic payment including insurance
            payment_schedule (str): weekly, biweekly, monthly
            amor_period (str):  Min 5 years, max 25 years
          
            Return:
            json: status code 400, error message
        """ 
        response = app.test_client().get(
            '/mortgage-amount', 
            query_string="payment_amount=449.13&payment_schedule=monthly&amor_period=1"
        )
        data = json.loads(response.get_data(as_text=True))
        assert response.status_code == 400
        assert data['Error'] == "something went wrong. Check your input."


    def test_interest_rate_succeed(self):
        """Test case where all parameters are correct and hence should succeed (status code 200)

            Params:
            json: interest rate to be updated

            Return:
            json: status code 200, old rate, new rate
        """ 
        response = app.test_client().patch(
            '/interest-rate',
            data=json.dumps({'interest_rate': 3.59}),
            content_type='application/json',
        )
        data = json.loads(response.get_data(as_text=True))
        assert response.status_code == 200
        assert data['old_interest_rate'] == 2.5
        assert data['new_interest_rate'] == 3.59

    def test_interest_rate_fail(self):
        """Test case where the parameter is incorrect and hence should fail (status code 400)

            Params:
            json: interest rate to be updated

            Return:
            json: status code 400, error message
        """ 
        response = app.test_client().patch(
            '/interest-rate',
            data=json.dumps({'interest_rate': 'new_interest_rate'}),
            content_type='application/json',
        )
        data = json.loads(response.get_data(as_text=True))
        assert response.status_code == 400
        assert data['Error'] == "something went wrong. Check your input."

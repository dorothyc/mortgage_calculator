# Mortgage Calculator
 Create a mortgage calculator API using Flask and RESTful APIs

## Set UP

git clone the project to working directory e.g. mortgage_calculator

navigate to the working directory

`cd mortgage_calculator`


install Flask using pip

`pip install Flask`


## Run the Application
run the Flask application 

`python api.py`

access the endpoints by going to the local host

http://127.0.0.1:5000/payment-amount?asking_price=50000&down_payment=20000&payment_schedule=monthly&amor_period=6
http://127.0.0.1:5000/mortgage-amount?payment_amount=449.13&payment_schedule=monthly&amor_period=6



## Run the unit tests
run the unit tests

`pytest test_mortgage_calc.py`


Please note error checking, exception handling and unit tests are performed but this is not an exhaustive list.




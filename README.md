# mortgage_calculator
 Create a mortgage calculator API using Flask RESTful

Run the Application

git clone the project to working directory e.g. mortgage_calculator

navigate to the working directory 
cd mortgage_calculator

run the Flask application with command
python api.py

access the endpoints by visiting:
http://127.0.0.1:5000/payment-amount?asking_price=50000&down_payment=20000&payment_schedule=monthly&amor_period=6
http://127.0.0.1:5000/mortgage-amount?payment_amount=449.13&payment_schedule=monthly&amor_period=6



Run the unit tests with command
pytest test_mortgage_calc.py


Please note error checking, exception handling and unit tests are performed but this is not an exhaustive list.




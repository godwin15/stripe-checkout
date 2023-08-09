#! /usr/bin/env python3.6
"""
Python 3.6 or newer required.
"""
import json
import configparser
import stripe

config = configparser.ConfigParser()
config.read('.env')
from flask import Flask, render_template, jsonify, request

public_key = config['ENV']['PUBLIC_KEY']
stripe.api_key = config['ENV']['STRIPE_KEY']


app = Flask(__name__, static_folder='public',
            static_url_path='/static', template_folder='templates/')


@app.route('/')
def home():
    return render_template('index.html', public_key=public_key)

@app.route('/thankyou')
def thankyou():
    return "Thank you"


@app.route('/payment', methods=['POST'])
def payment():
    #CUSTOMER INFO
    amount = request.form['amount']
    amount=int(float(amount) * 100)
    customer = stripe.Customer.create(email =request.form['stripeEmail'], source=request.form['stripeToken'])
    #PAYMENT INFO
    charge = stripe.Charge.create(
        customer=customer.id,
        amount=amount, 
        currency='usd',
        description='Giving to SCC'
    )
    return "Thank you"

#checkout method
@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    amount = request.json['amount']

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'unit_amount': amount,
                'product_data': {
                    'name': 'Giving to SCC',
                },
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.url_root + 'thankyou',
        cancel_url=request.url_root,
    )

    return {'id': session.id}

if __name__ == '__main__':
    app.run(port=4242, debug=True)
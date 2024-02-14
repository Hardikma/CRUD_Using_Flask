# app.py

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import re

# Regular expression to validate a phone number with ten digits
phone_number_pattern = re.compile(r'^\d{10}$')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'hardikAPISecretKey#123Demo'  # Change this to a random secret key
db = SQLAlchemy(app)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    number = db.Column(db.String(15), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    employees = Employee.query.all()
    return render_template('index.html', employees=employees)

@app.route('/add', methods=['POST'])
def add():
    try:
        name = request.form['name']
        email = request.form['email']
        number = request.form['number']

        if not (phone_number_pattern.match(number) and len(number) == 10):
            flash('Invalid phone number. Please enter a valid 10-digit phone number.', 'error')
            return redirect(url_for('index'))

        new_employee = Employee(name=name, email=email, number=number)
        db.session.add(new_employee)
        db.session.commit()
        flash('Employee added successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error adding employee: {str(e)}', 'error')
    return redirect(url_for('index'))

@app.route('/edit/<int:employee_id>', methods=['GET', 'POST'])
def edit(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    if request.method == 'POST':
        try:
            employee.name = request.form['name']
            employee.email = request.form['email']
            employee.number = request.form['number']
            db.session.commit()
            flash('Employee updated successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating employee: {str(e)}', 'error')
        return redirect(url_for('index'))
    return render_template('edit.html', employee=employee)

@app.route('/delete/<int:employee_id>')
def delete(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    try:
        db.session.delete(employee)
        db.session.commit()
        flash('Employee deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting employee: {str(e)}', 'error')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

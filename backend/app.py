from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)  # Enable CORS for frontend

# SQLite Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employees.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Employee Model
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    department = db.Column(db.String(100), nullable=False)

# Create Database Tables
with app.app_context():
    db.create_all()

# Home Route (Fixes 404 Error)
@app.route('/')
def home():
    return "Flask Backend is Running!", 200  # Simple text response

# Serve Frontend from Flask
@app.route('/ui')
def serve_frontend():
    return render_template("index.html")

# Get All Employees
@app.route('/employees', methods=['GET'])
def get_employees():
    employees = Employee.query.all()
    return jsonify([{'id': e.id, 'name': e.name, 'email': e.email, 'department': e.department} for e in employees])

# Add Employee
@app.route('/employees', methods=['POST'])
def add_employee():
    data = request.json
    if not all(key in data for key in ["name", "email", "department"]):
        return jsonify({'error': 'Missing data'}), 400
    new_employee = Employee(name=data['name'], email=data['email'], department=data['department'])
    db.session.add(new_employee)
    db.session.commit()
    return jsonify({'message': 'Employee added successfully!'}), 201

# Update Employee
@app.route('/employees/<int:id>', methods=['PUT'])
def update_employee(id):
    data = request.json
    employee = Employee.query.get(id)
    if employee:
        employee.name = data['name']
        employee.email = data['email']
        employee.department = data['department']
        db.session.commit()
        return jsonify({'message': 'Employee updated successfully!'})
    return jsonify({'message': 'Employee not found'}), 404

# Delete Employee
@app.route('/employees/<int:id>', methods=['DELETE'])
def delete_employee(id):
    employee = Employee.query.get(id)
    if employee:
        db.session.delete(employee)
        db.session.commit()
        return jsonify({'message': 'Employee deleted successfully!'})
    return jsonify({'message': 'Employee not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

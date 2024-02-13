from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/kainApp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma=Marshmallow(app)

class Customer(db.Model):
    C_id = db.Column(db.Integer, primary_key=True)
    C_name = db.Column(db.String(100), nullable=False)
    C_email = db.Column(db.String(100), nullable=False)
    C_phone = db.Column(db.Integer, nullable=False)
    C_address = db.Column(db.String(100), nullable=False)

    def __init__(self, name, email, phone, address):
        self.C_name = name
        self.C_email = email
        self.C_phone = phone
        self.C_address = address
    
class CustomerSchema (ma.Schema):
        class Meta:
            fields = ('C_id','C_name','C_email','C_phone','C_address')

customer_schema=CustomerSchema()
customer_schema=CustomerSchema()
 

@app.route('/get', methods=['GET'])
def get_Customer():
    all_Customers = Customer.query.all()
    customer_schema = CustomerSchema(many=True)  # Create a schema instance with many=True
    results = customer_schema.dump(all_Customers)  # Use the schema instance to dump the data
    return jsonify(results)

@app.route('/get/<id>/', methods=['GET'])
def get_Customerbyid(id):
    customer = Customer.query.get(id)
    customer_schema = CustomerSchema()  # Create a schema instance with many=True
    results = customer_schema.dump(customer)  # Use the schema instance to dump the data
    return jsonify(results)

@app.route('/add', methods=['post'])
def add_customer():
    name=request.json['name']
    email=request.json['email']
    phone=request.json['phone']
    address=request.json['address']

    customer=Customer(name, email, phone, address)
    db.session.add(customer)
    db.session.commit()
    return customer_schema.jsonify(customer)

@app.route('/update/<id>/', methods=['PUT'])
def update_customer(id):
    # Query for the customer
    customer = Customer.query.get(id)
    
    if not customer:
        return {"error": "Customer not found"}, 404

    # Update the customer's attributes
    if 'name' in request.json:
        customer.C_name = request.json['name']
    if 'email' in request.json:
        customer.C_email = request.json['email']
    if 'phone' in request.json:
        customer.C_phone = request.json['phone']
    if 'address' in request.json:
        customer.C_address = request.json['address']

    # Commit the changes to the database
    try:
        db.session.commit()
    except Exception as e:
        return {"error": str(e)}, 500

    # Return the updated customer
    return customer_schema.jsonify(customer)



@app.route("/delete/<id>/",methods=["DELETE"])
def customer_delete(id):
    customer=Customer.query.get(id)
    db.session.delete(customer)
    db.session.commit()
    return customer_schema.jsonify(customer)






if __name__ == "__main__":
    with app.app_context(): 
        db.create_all()  
    app.run(debug=True)

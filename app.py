from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///parts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Part model
class Part(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(80), nullable=False)
    model = db.Column(db.String(120), nullable=False)
    specification = db.Column(db.String(250))
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Part {self.model}>'

# Initialize the database and create tables
@app.before_first_request
def create_tables():
    db.create_all()

# Endpoint to add a new part
@app.route('/parts', methods=['POST'])
def add_part():
    data = request.get_json()
    new_part = Part(
        type=data['type'],
        model=data['model'],
        specification=data.get('specification', ''),
        price=data['price']
    )
    db.session.add(new_part)
    db.session.commit()
    return jsonify({
        'id': new_part.id,
        'type': new_part.type,
        'model': new_part.model,
        'specification': new_part.specification,
        'price': new_part.price
    }), 201

# Endpoint to get all parts
@app.route('/parts', methods=['GET'])
def get_parts():
    parts = Part.query.all()
    parts_list = [{
        'id': part.id,
        'type': part.type,
        'model': part.model,
        'specification': part.specification,
        'price': part.price
    } for part in parts]
    return jsonify(parts_list), 200

s
if __name__ == '__main__':
    app.run(debug=True)

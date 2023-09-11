"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planets, Vehicles, Favorites

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route('/people', methods=['GET'])
def handle_people():
    return "hello people"

@app.route('/people/<int:person_id>', methods=['PUT', 'GET'])
def get_single_person(person_id):
    if request.method == 'GET':
        person1 = People.query.get(person_id)
        return jsonify(person1.serialize()), 200
    
    return "Person not found", 404

@app.route('/planets', methods=['GET'])
def handle_planets():
    return "hello planets"

@app.route('/planets/<int:planets_id>', methods=['PUT', 'GET'])
def get_single_planet(planets_id):
    if request.method == 'GET':
        planet1 = Planets.query.get(planets_id)
        return jsonify(planet1.serialize()), 200
    
    return "Person not found", 404


@app.route('/vehicles', methods=['GET'])
def handle_vehicles(vehicles_id):
     if request.method == 'GET':
        vehicles = map(Vehicles, Vehicles.query.get(vehicles_id))
        return jsonify(vehicles.serialize()), 200
     
@app.route('/vehicles/<int:vehicles_id>', methods=['PUT', 'GET'])
def get_single_vehicle(vehicles_id):
    if request.method == 'GET':
        vehicle1 = Vehicles.query.get(vehicles_id)
        return jsonify(vehicle1.serialize()), 200
    
    return "Person not found", 404





# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
